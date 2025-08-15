import argparse
import pytest
import json


def construct(file_str: str) -> dict[str, dict[str, float]]:
    """Takes in the string representing the file and returns pfsa
    The given example is for the statement "A cat"
    """
    # TODO: FILE IN THIS FUNCTION
    lst = file_str.splitlines()
    unique_words = []
    pfsa = {}
    done_traversing_dict = []

    for s in lst:
        words = s.lower().split()
        for i in words:
            # if i not in unique_words:
            unique_words.append(i)
    # print(unique_words)
    pfsa["*"]={}
    prev_key = "*"
    i=1
    for substr in unique_words:
        if substr[0] not in pfsa[prev_key]:
            pfsa[prev_key][substr[0]] = 1.0
    
    cnt = 0
    l = len(unique_words)
    for i in pfsa["*"]:
        for j in unique_words:
            if j[0]==i:
                cnt += 1
        pfsa['*'][i]=cnt/l
        cnt = 0
    # count = 0
   
    keys_list = list(pfsa.keys())

    all_words_in_pfsa = all([elem in keys_list for elem in unique_words])
    while all_words_in_pfsa == False:
        dict1 = pfsa[prev_key]
        done_traversing_dict.append(prev_key)
        
        for substr in list(dict1.keys()):
            if substr.endswith("*") == False:
                dict2={}
                for word in unique_words:
                    if word.startswith(substr):
                        if word == substr:
                            dict2[word+"*"] = 1.0
                        else:
                            dict2[word[0:len(substr)+1]] = 1.0
                for i in dict2:
                    count_i = 0
                    count_parent = 0
                    if i.endswith("*") == False:
                        for w in unique_words:
                            if w.startswith(i):
                                count_i += 1
                            if w.startswith(substr):
                                count_parent += 1
                    else:
                        for w in unique_words:
                            if w==i[:-1]:
                                count_i += 1
                            if w.startswith(substr):
                                count_parent += 1
                    dict2[i] = count_i/count_parent
                    
                pfsa[substr] = dict2
                
                
            else:
                continue

        keys_list = list(pfsa.keys())
        for key in keys_list:
            if key not in done_traversing_dict:
                prev_key = key
                break

        all_words_in_pfsa = all([elem in keys_list for elem in unique_words])

    return pfsa

        
        

    # return {
    #     "*": {"a": 0.5, "c": 0.5},
    #     "a": {"a*": 1.0},
    #     "c": {"ca": 1.0},
    #     "ca": {"cat": 1.0},
    #     "cat": {"cat*": 1.0},
    # }
    


def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="text_sample.txt")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file, indent = 1)


if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.
    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = construct(string)
    assert result == pfsa
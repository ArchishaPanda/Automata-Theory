import re 
from termcolor import colored
##################### BOILERPLATE BEGINS ############################

# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################
class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"

# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# helper function to check if it is a valid identifier

def is_valid_identifier(lexeme):
    # -1 for empty
    # -2 for first character is an underscore or a letter
    # -3 for rest of the characters (can be letters, digits, or underscores)
        
    if not lexeme:
        return False
        # return -1

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False
        # return -2

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False
            # return -3
    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char=='_')

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    # if value == -1:
                    #     print(colored("Identifier cannot be empty","orange"))
                    # elif value == -2:
                    #     print(colored("First character can only be an underscore or a letter","orange"))
                    # elif value == -3:
                    #     print(colored("Characters can be letters, digits, or underscores only","orange"))

                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position+1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens

########################## BOILERPLATE ENDS ###########################

# def check_tokens(tokens,argument):
#     for tup in tokens:
#         if tup[1] == argument:
#             return tup[0]

def check_brackets(source_code):
    open = 0
    close = 0
    for i in source_code:
        if i=='(':
            open += 1
        if i==')':
            close += 1
    return open==close

def split_acc_to_bracket(input_string):
    
    bracket_count = 0
    start_index = None
    
    extracted_strings = []    
    for i, char in enumerate(input_string):
        if char == "(":         
            if bracket_count == 0:
                start_index = i+1
            bracket_count += 1
        elif char == ")":            
            bracket_count -= 1
            if bracket_count == 0:
                extracted_strings.append(input_string[start_index:i])

    return extracted_strings

def check_y(line,tokens):
    for tup in tokens:
        if tup[1]==line:
            if tup[0] in ["FLOAT","INTEGER","KEYWORD","IDENTIFIER"] and tup[1] not in ["if","else"]:
                return True
            else:
                return False

def check_x(line,tokens):
    if check_y(line,tokens):
        return True
    if check_syntax_for_condition(line,tokens):
        return True
    return False
           
def check_syntax_for_condition(line,tokens):
    operators = ["+","-","*","/","^","<",">","="]

    result = split_acc_to_bracket(line)
    # print(result)
    if result == [] or len(result)>3 or len(result)==2:
        print(colored("Syntax Error: Invalid syntax for condition.","red"))   

    if len(result)==3:
        flag1 = check_x(result[0],tokens)
        flag2 = result[1] in operators
        flag3 = check_x(result[2],tokens)
        if flag1 and flag2 and flag3:
            return True
        else:
            return False
    
    elif len(result)==1:
        return check_x(result[0],tokens)

def check_A(line,tokens):

    result_list = split_acc_to_bracket(line)
    # print(result_list)

    if "else" not in result_list:
        if len(result_list)<2:
            print(colored("Syntax Error: if must be followed with a condition and statement","red"))   #error
            return False

        if len(result_list)>2:
            print(colored("Syntax Error: if cannot be followed with multiple conditions or statements","red"))   #error
            return False
        
        flag1 = check_syntax_for_condition(result_list[0],tokens)
        flag2 = check_statement(result_list[1],tokens)
        if flag1 and flag2:
            return True
        if flag1 == False:
            print(colored("Syntax Error: Invalid condition","red"))        #error
        if flag2 == False:
            print(colored("Syntax Error: Invalid statement in 'if'","red"))    #error        
        return False
    
    else:
        if len(result_list)<4:
            print(colored("Syntax Error: Wrong syntax for if...else","red"))
            return False
        
        if len(result_list)>4:
            print(colored("Syntax Error: Wrong syntax for if...else","red"))
            return False
        
        flag1 = check_syntax_for_condition(result_list[0],tokens)
        flag2 = check_statement(result_list[1],tokens)
        flag3 = ("else"==result_list[2])
        flag4 = check_statement(result_list[3],tokens)
        if flag1 and flag2 and flag3 and flag4:
            return True
        if flag1 == False:
            print(colored("Syntax Error: Invalid condition","red"))
        if flag2 == False:
            print(colored("Syntax Error: Invalid statement","red"))
        if flag3 == False:
            print(colored("Syntax Error: else is not used correctly in accordance with if","red"))
        if flag4 == False:
            print(colored("Syntax Error: Invalid statement","red"))
        return False

def check_statement(line,tokens):
    if line.startswith("if"):
        return check_A(line[3:],tokens)
    
    elif line[0]!='(':
        command = line.split()
        for comm in command:
            for tup in tokens:
                if tup[1] == comm:
                    if tup[0] in ["KEYWORD","FLOAT","INTEGER","IDENTIFIER"] and tup[1] not in ["if","else"]:
                        break
                    else:
                        if tup[1]=="else":
                            print(colored("Syntax Error: Incorrect use of 'else'","red"))
                            return False
                        if tup[0]=="SYMBOL":
                            print(colored("Syntax Error: Statement cannot contain symbols","red"))
                            return False
                        return False
        return True
    
    else:
        words = split_acc_to_bracket(line)
        for word in words:
            if check_statement(word,tokens):
                continue
            else:
                return False
        return True

def checkGrammar(source_code,tokens):
    # write the code the syntactical analysis in this function
    # You CAN use other helper functions and create your own helper functions if needed  
    return check_statement(source_code,tokens)
     



# Test the tokenizer
if __name__ == "__main__":
    # source_code = "if 2+xi > 0 print 2.0 else print -1;"
    source_code = input()
    tokens = tokenize(source_code)                              # Tokens is a list of tuples

    if check_brackets(source_code) != True:
        print(colored("Syntax Error: Imbalance in opening and closing brackets","red"))    # Error
        exit(0)
    # for token in tokens:
    #     print(f"Token Type: {token[0]}, Token Value: {token[1]}") 
           
    
    logs = checkGrammar(source_code,tokens)  # You are tasked with implementing the function checkGrammar
    if logs == True:
        for token in tokens:
            print(f"Token Type: {token[0]}, Token Value: {token[1]}")  
  
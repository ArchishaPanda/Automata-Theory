Compilers form an integral part of any programming language or any computer system in general. Following is a very elementary implmentation of a compiler using concepts of Tokenization and CFG Parsing. Due to the simplicity in codebase of the compiler, there are certain limitations and restrictions within the framework of the compiler. The purpose of this README is to familiarise you with these limitations and also describe the fundamentals of the program.

The compiler checks syntactical correctness on the basis of the following context free grammar:
    Rule 1:         S           -> statement
    Rule 2:         statement   -> if A | (statement)(statement) | y
    Rule 3:         A           -> (condition)(statement) | (condition)(statement)(else)(statement)
    Rule 4:         condition   -> (x)(op1)(x) | (x)
    Rule 5:         op1         -> + | - | * | / | ^ | < | > | =
    Rule 6:         x           -> R(real numbers) | condition | y
    Rule 7:         y            ∈ statement alphabets [Σstatement ]

    Σstatement = numbers U keywords U identifiers - {’if ’ , ’else’}

The grammar above needs to be strictly followed (including the brackets) for the code to be accepted by the compiler. 
For example:
if (x>0)(print x) - Syntax Error
Correct syntax - if ((x)(>)(0))(print x)    [according to Rule 2 and 7]

Certain assumptions:
    1. The compiler does not supprt operations like '>=' and '<='
    2. 'if' must be followed by a space as shown in grammar Rule 2
    3. Nowhere in the code do you need to use a semi-colon (;)
    4. Negetive numbers are not considered as integers due to '-' being identified as symbol in parser
    5. If the compiler doesn't print anything it is an indication of an error
    6. Any two separate tokens must be separated by a space. Exampple '+=' won't be considered as 2 symbols    unless given as '+ ='

Explanation of the Code:
    Input is taken from the user
    Input is tokenised into IDENTIFIERS, FLOAT, INTEGERS, KEYWORD, SYMBOL. The tokens are stored as a list of tuples.
    Tokens and source_code are passed into check_grammar function.

    Helper Functions defined and used:
    check_brackets : To check the balance of brackets in the input
    split_acc_to_bracket : Extract string from within brackets to analyze further
    check_y : Check if it satisfies grammar rule 7
    check_x : Check if it satisfies grammar rule 6
    check_syntax_for_condition : Evaluate rule 4
    check_A : Verify rule 3
    check_statement : Verify rule 2

    Main Idea: Try to simulate a possible derivation of the input. If any grammar rule is violated anywhere in the process, raise a syntax error.




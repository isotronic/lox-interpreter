import sys
import pathlib
# from constants import TokenType, SINGLE_CHAR_TOKENS, RESERVED_WORDS
from enum import Enum, auto

class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DOT = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    SLASH = auto()
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    EOF = auto()

RESERVED_WORDS = ["and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"]

SINGLE_CHAR_TOKENS = {
    '(': TokenType.LEFT_PAREN,
    ')': TokenType.RIGHT_PAREN,
    '{': TokenType.LEFT_BRACE,
    '}': TokenType.RIGHT_BRACE,
    ',': TokenType.COMMA,
    ';': TokenType.SEMICOLON,
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.STAR,
    '.': TokenType.DOT,
}

def scan_file(contents):
    """
    Scans a file and prints out tokens based on the contents of the file.

    Parameters:
        contents (str): The contents of the file to be scanned.

    Returns:
        bool: True if there was an error during the scanning process, False otherwise.
    """
    line_number = 1 # To track the current line number in the input file
    has_error = False # Flag to indicate if any error occurred during scanning
    index = 0 # Index to iterate through the file contents
    
    def peek_next_char(index):
        """
        A function that returns the next character in the content if available.
        """
        return contents[index + 1] if index < len(contents) - 1 else None
    
    def handle_string(index):
        """
        A function that handles string tokens in the contents.

        Parameters:
            index (int): The index to start processing the string from.

        Returns:
            int: The index after processing the string.
        """
        start = index
        index += 1 # Skip the opening quote
        while index < len(contents) and contents[index] != "\"":
            if contents[index] == "\n":
                nonlocal line_number
                line_number += 1 # Increment line number if newline character is within the string
            index += 1
        
        if index < len(contents):
            string_value = contents[start+1:index]
            print(f"{TokenType.STRING.name} \"{string_value}\" {string_value}")
        else:
            print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)
            nonlocal has_error
            has_error = True
        return index
    
    def handle_number(index):
        """
        A function that handles number tokens in the contents.

        Parameters:
            index (int): The starting index of the number in the string.

        Returns:
            int: The index after processing the number.
        """
        start = index
        has_decimal = False # Flag to check if a decimal point has been encountered
        if contents[index] == '.':
            has_decimal = True
        index += 1
        while index < len(contents) and (contents[index].isdigit() or (contents[index] == '.' and not has_decimal)):
            if contents[index] == ".":
                if has_decimal:
                    break # Break if more than one decimal point is encountered
                has_decimal = True
            index += 1
        number = contents[start:index]
        print(f"{TokenType.NUMBER.name} {number.rstrip('.')} {float(number)}")
        if number.endswith('.') and (index >= len(contents) or not contents[index].isdigit()):
            print(f"{TokenType.DOT.name} . null")
        elif index < len(contents) and contents[index] == ".":
            print(f"{TokenType.DOT.name} . null")
        else:
            index -= 1
        return index
    
    def handle_identifier_or_keyword(index):
        """
        A function that handles identifiers or keywords in the contents.

        Parameters:
            index (int): The starting index of the identifier or keyword in the string.

        Returns:
            int: The index after processing the identifier or keyword.
        """
        start = index
        index += 1
        while index < len(contents) and (contents[index].isalpha() or contents[index].isdigit() or contents[index] == "_"):
            index += 1
        name = contents[start:index]
        if name in RESERVED_WORDS:
            print(f"{name.upper()} {name} null")
        else:
            print(f"{TokenType.IDENTIFIER.name} {name} null")
        return index - 1
    
    while index < len(contents):
        char = contents[index]
        
        if char.isspace():
            if char == "\n":
                line_number += 1
            index += 1
            continue
        
        if char in SINGLE_CHAR_TOKENS:
            print(f"{SINGLE_CHAR_TOKENS[char].name} {char} null")
        elif char == "=":
            if peek_next_char(index) == "=":
                print(f"{TokenType.EQUAL_EQUAL.name} == null")
                index += 1
            else:
                print(f"{TokenType.EQUAL.name} = null")
        elif char == "!":
            if peek_next_char(index) == "=":
                print(f"{TokenType.BANG_EQUAL.name} != null")
                index += 1
            else:
                print(f"{TokenType.BANG.name} ! null")
        elif char == "<":
            if peek_next_char(index) == "=":
                print(f"{TokenType.LESS_EQUAL.name} <= null")
                index += 1
            else:
                print(f"{TokenType.LESS.name} < null")
        elif char == ">":
            if peek_next_char(index) == "=":
                print(f"{TokenType.GREATER_EQUAL.name} >= null")
                index += 1
            else:
                print(f"{TokenType.GREATER.name} > null")
        elif char == "/":
            if peek_next_char(index) == "/":
                while index < len(contents) and contents[index] != "\n":
                    index += 1
                line_number += 1
            else:
                print(f"{TokenType.SLASH.name} / null")
        elif char == "\"":
            index = handle_string(index)
        elif char.isdigit() or (char == '.' and peek_next_char() and peek_next_char().isdigit()):
            index = handle_number(index)
        elif char.isalpha() or char == "_":
            index = handle_identifier_or_keyword(index)
        else:
            print(f"[line {line_number}] Error: Unexpected character: {char}", file=sys.stderr)
            has_error = True

        index += 1
        
    return has_error

def main():
    """
    The main function of the program.

    This function is responsible for parsing command line arguments and executing the tokenization process.

    Raises:
        SystemExit: If the command line arguments are invalid or the command is unknown.
    """
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    file_contents = pathlib.Path(filename).read_text()
  
    has_error = scan_file(file_contents)
    
    print(f"{TokenType.EOF.name}  null")
    
    if has_error:
        exit(65)


if __name__ == "__main__":
    main()

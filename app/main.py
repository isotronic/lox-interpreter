import sys
import pathlib

RESERVED_WORDS = ["and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"]
SINGLE_CHAR_TOKENS = {
    '(': 'LEFT_PAREN',
    ')': 'RIGHT_PAREN',
    '{': 'LEFT_BRACE',
    '}': 'RIGHT_BRACE',
    ',': 'COMMA',
    ';': 'SEMICOLON',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'STAR',
    '.': 'DOT',
}

def scan_file(contents):
    """
    Scans a file and prints out tokens based on the contents of the file.

    Parameters:
        contents (str): The contents of the file to be scanned.

    Returns:
        bool: True if there was an error during the scanning process, False otherwise.
    """
    line_number = 1
    has_error = False
    i = 0
    
    def peek_next_char(i):
        """
        A function that returns the next character in the content if available.
        """
        return contents[i + 1] if i < len(contents) - 1 else None
    
    def handle_string(i):
        """
        A function that handles string tokens in the contents.

        Parameters:
            i (int): The index to start processing the string from.

        Returns:
            int: The index after processing the string.
        """
        start = i
        i += 1
        while i < len(contents) and contents[i] != "\"":
            if contents[i] == "\n":
                nonlocal line_number
                line_number += 1
            i += 1
        
        if i < len(contents):
            string_value = contents[start+1:i]
            print(f"STRING \"{string_value}\" {string_value}")
        else:
            print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)
            nonlocal has_error
            has_error = True
        return i
    
    def handle_number(i):
        """
        A function that handles number tokens in the contents.

        Parameters:
            i (int): The starting index of the number in the string.

        Returns:
            int: The index after processing the number.
        """
        start = i
        has_decimal = False
        if contents[i] == '.':
            has_decimal = True
        i += 1
        while i < len(contents) and (contents[i].isdigit() or (contents[i] == '.' and not has_decimal)):
            if contents[i] == ".":
                if has_decimal:
                    break
                has_decimal = True
            i += 1
        number = contents[start:i]
        print(f"NUMBER {number.rstrip('.')} {float(number)}")
        if number.endswith('.') and (i >= len(contents) or not contents[i].isdigit()):
            print("DOT . null")
        elif i < len(contents) and contents[i] == ".":
            print("DOT . null")
        else:
            i -= 1
        return i
    
    def handle_identifier_or_keyword(i):
        """
        A function that handles identifiers or keywords in the contents.

        Parameters:
            i (int): The starting index of the identifier or keyword in the string.

        Returns:
            int: The index after processing the identifier or keyword.
        """
        start = i
        i += 1
        while i < len(contents) and (contents[i].isalpha() or contents[i].isdigit() or contents[i] == "_"):
            i += 1
        name = contents[start:i]
        if name in RESERVED_WORDS:
            print(f"{name.upper()} {name} null")
        else:
            print(f"IDENTIFIER {name} null")
        return i - 1
    
    while i < len(contents):
        char = contents[i]
        
        if char.isspace():
            if char == "\n":
                line_number += 1
            i += 1
            continue
        
        if char in SINGLE_CHAR_TOKENS:
            print(f"{SINGLE_CHAR_TOKENS[char]} {char} null")
        elif char == "=":
            if peek_next_char(i) == "=":
                print("EQUAL_EQUAL == null")
                i += 1
            else:
                print("EQUAL = null")
        elif char == "!":
            if peek_next_char(i) == "=":
                print("BANG_EQUAL != null")
                i += 1
            else:
                print("BANG ! null")
        elif char == "<":
            if peek_next_char(i) == "=":
                print("LESS_EQUAL <= null")
                i += 1
            else:
                print("LESS < null")
        elif char == ">":
            if peek_next_char(i) == "=":
                print("GREATER_EQUAL >= null")
                i += 1
            else:
                print("GREATER > null")
        elif char == "/":
            if peek_next_char(i) == "/":
                while i < len(contents) and contents[i] != "\n":
                    i += 1
                line_number += 1
            else:
                print("SLASH / null")
        elif char == "\"":
            i = handle_string(i)
        elif char.isdigit() or (char == '.' and peek_next_char() and peek_next_char().isdigit()):
            i = handle_number(i)
        elif char.isalpha() or char == "_":
            i = handle_identifier_or_keyword(i)
        else:
            print(f"[line {line_number}] Error: Unexpected character: {char}", file=sys.stderr)
            has_error = True

        i += 1
        
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
    
    print("EOF  null")
    
    if has_error:
        exit(65)


if __name__ == "__main__":
    main()

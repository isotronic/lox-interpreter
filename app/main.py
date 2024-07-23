import sys
import pathlib

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
    
    def peek_next_char():
        """
        A function that returns the next character in the content if available.
        """
        return contents[i + 1] if i < len(contents) - 1 else None
    
    while i < len(contents):
        char = contents[i]
        
        if char.isspace():
            if char == "\n":
                line_number += 1
            i += 1
            continue
        
        if char == "(":
            print("LEFT_PAREN ( null")
        elif char == ")":
            print("RIGHT_PAREN ) null")
        elif char == "{":
            print("LEFT_BRACE { null")
        elif char == "}":
            print("RIGHT_BRACE } null")
        elif char ==",":
            print("COMMA , null")
        elif char == ";":
            print("SEMICOLON ; null")
        elif char == "+":
            print("PLUS + null")
        elif char == "-":
            print("MINUS - null")
        elif char == "*":
            print("STAR * null")
        elif char == ".":
            print("DOT . null")
        elif char == "=":
            if peek_next_char() == "=":
                print("EQUAL_EQUAL == null")
                i += 1
            else:
                print("EQUAL = null")
        elif char == "!":
            if peek_next_char() == "=":
                print("BANG_EQUAL != null")
                i += 1
            else:
                print("BANG ! null")
        elif char == "<":
            if peek_next_char() == "=":
                print("LESS_EQUAL <= null")
                i += 1
            else:
                print("LESS < null")
        elif char == ">":
            if peek_next_char() == "=":
                print("GREATER_EQUAL >= null")
                i += 1
            else:
                print("GREATER > null")
        elif char == "/":
            if peek_next_char() == "/":
                while i < len(contents) and contents[i] != "\n":
                    i += 1
                line_number += 1
            else:
                print("SLASH / null")
        elif char == "\"":
            start = i
            i += 1
            while i < len(contents) and contents[i] != "\"":
                if contents[i] == "\n":
                    line_number += 1
                i += 1
            
            if i < len(contents):
                string_value = contents[start+1:i]
                print(f"STRING \"{string_value}\" {string_value}")
            else:
                print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)
                has_error = True
            i += 1
        elif char.isdigit():
            start = i
            has_decimal = False
            while i < len(contents) and (contents[i].isdigit() or (contents[i] == "." and not has_decimal)):
                if contents[i] == ".":
                    has_decimal = True
                    if i + 1 >= len(contents) or not contents[i+1].isdigit():
                        print(f"NUMBER {contents[start:i]} {contents[start:i]}")
                        i += 1
                        break
                i += 1
            if has_decimal and (i < len(contents) and not contents[i].isdigit()):
                i = start + contents[start:i].find(".")
            else:
                if i < len(contents) and contents[i].isalpha():
                    print(f"[line {line_number}] Error: Invalid number format.", file=sys.stderr)
                    has_error = True
                else:
                    number = contents[start:i]
                    print(f"NUMBER {number} {number}")
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

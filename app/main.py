import sys
import pathlib

def scan_file(contents):
    line_number = 1
    has_error = False
    
    for char in contents:
        if char == "\n":
            line_number += 1
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
            print("EQUAL = null")
        elif char == "==":
            print("EQUAL_EQUAL == null")
        elif char == "<":
            print("LESS < null")
        elif char == ">":
            print("GREATER > null")
        elif char == "<=":
            print("LESS_EQUAL <= null")
        elif char == ">=":
            print("GREATER_EQUAL >= null")
        elif char == "!=":
            print("BANG_EQUAL != null")
        else:
            print(f"[line {line_number}] Error: Unexpected character: {char}", file=sys.stderr)
            has_error = True
        
    return has_error

def main():
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

import sys

from toy.interpreter import Interpreter
from toy.lexer import Lexer
from toy.parser import Parser

interpreter = Interpreter()


def run(source: str):
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        for expr in ast:
            value = interpreter.evaluate(expr)
            print(value)
    except (SyntaxError, RuntimeError) as e:
        print(f"Error: {e}")


def run_file(path: str):
    with open(path, "r") as f:
        source = f.read()
    run(source)


def repl():
    print("Toy Language REPL")
    print("type 'exit' to quit\n")

    while True:
        line = input(">>> ")
        if line.strip() == "exit":
            break
        run(line)


def main():
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()


if __name__ == "__main__":
    main()

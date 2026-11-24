import pytest

from toy.ast_nodes import *
from toy.interpreter import Interpreter
from toy.lexer import Lexer
from toy.parser import Parser
from toy.tokens import Token, TokenType


def test_lexer_tokenize():
    source = "3 + 2"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens == [
        Token(TokenType.NUMBER, "3", 1),
        Token(TokenType.PLUS, "+", 1),
        Token(TokenType.NUMBER, "2", 1),
        Token(TokenType.EOF, "", 1),
    ]


def test_lexer_tokenize_ignored_chars():
    source = "2\t * 3\n / 4"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens == [
        Token(TokenType.NUMBER, "2", 1),
        Token(TokenType.STAR, "*", 1),
        Token(TokenType.NUMBER, "3", 1),
        Token(TokenType.SLASH, "/", 2),
        Token(TokenType.NUMBER, "4", 2),
        Token(TokenType.EOF, "", 2),
    ]

def tokenize(source: str) -> list[Token]:
    """Tokenize source code."""
    lexer = Lexer(source)
    return lexer.tokenize()


def parse(source: str) -> list:
    """Parse source code into AST."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def evaluate(source: str):
    """Evaluate source code and return result."""
    ast = parse(source)
    interpreter = Interpreter()
    result = None
    for statement in ast:
        result = interpreter.evaluate(statement)
    return result

# Interpreter tests
@pytest.mark.parametrize(
    "source,expected",
    [
        ("3 + 2 * 4;", 11.0),  # Precedence: 3 + (2 * 4)
        ("3 + 2 > 4;", True),  # Comparison: 5 > 4
        ("3 + 2 == 5;", True),  # Equality: 5 == 5
        ("3 + 2 == 4;", False),  # Equality: 5 == 4
        ("-2 + 3;", 1),  # Unary: 1
    ],
)
def test_evaluate_expressions(source, expected):
    assert evaluate(source) == expected

def test_parse_var_declaration():
    ast = parse("var a = 1;")
    assert ast == [
        VarStatement(
            Token(TokenType.IDENTIFIER, "a", 1),
            Literal(1.0),
        )
    ]
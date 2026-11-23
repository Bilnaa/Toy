from dataclasses import dataclass
from enum import StrEnum, auto


class TokenType(StrEnum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str  # String du symbol original (e.g "+", "0901")
    line: int


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def tokenize(source: str) -> list[Token]:
    """No code comprehension is needed here"""
    tokens = []
    line_number = 1
    for line in source.splitlines():
        # for each "word" in the line, we'll have a token
        for word in line.split():
            match word:
                case word if is_number(word):
                    tokens.append(Token(TokenType.NUMBER, word, line_number))
                case "+":
                    tokens.append(Token(TokenType.PLUS, word, line_number))
                case "-":
                    tokens.append(Token(TokenType.MINUS, word, line_number))
                case "*":
                    tokens.append(Token(TokenType.MULT, word, line_number))
                case "/":
                    tokens.append(Token(TokenType.DIV, word, line_number))
        line_number += 1
    return tokens


@dataclass
class EvalResult:
    value: int | float
    index: int  # index of the next token that we need to evaluate


def evaluate(tokens: list[Token], index: int = 0) -> EvalResult:
    # [+ 1 2]
    token = tokens[index]
    if token.type == TokenType.NUMBER:
        return EvalResult(value=float(token.lexeme), index=index + 1)
    # we evaluate our 2 operands (left and right)
    left_result = evaluate(tokens, index + 1)
    right_result = evaluate(tokens, left_result.index)
    next_index = right_result.index
    match token.type:
        case TokenType.PLUS:
            return EvalResult(
                value=left_result.value + right_result.value,
                index=next_index)
        case TokenType.MINUS:
            return EvalResult(
                value=left_result.value - right_result.value,
                index=next_index)
        case TokenType.MULT:
            return EvalResult(
                value=left_result.value * right_result.value,
                index=next_index)
        case TokenType.DIV:
            # if we div by 0, it's impossible so we don't even bother lol
            if right_result.value == 0:
                raise ValueError(f"Division by zero is not possible, Operands are {left_result.value} and {right_result.value}")
            return EvalResult(
                value=left_result.value / right_result.value,
                index=next_index)
        case _:
            raise ValueError(f"Unknown token type {token.type}")


def calculate(source: str) -> int | float:
    tokens = tokenize(source)
    if not tokens:
        raise ValueError(f"No tokens were found")
    result = evaluate(tokens)
    return result.value


def main():
    pass

if __name__ == "__main__":
    main()

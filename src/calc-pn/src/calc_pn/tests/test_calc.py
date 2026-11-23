# test_calc.py
from calc_pn.calc import Token, TokenType, tokenize, calculate
import pytest


def test_tokenizer_empty_source_noop():
    source = ""
    assert tokenize(source) == []


def test_tokenizer_simple_addition():
    source = "+ 1 2"
    assert tokenize(source) == [
        Token(TokenType.PLUS, "+", 1),
        Token(TokenType.NUMBER, "1", 1),
        Token(TokenType.NUMBER, "2", 1),
    ]

def test_calculate_empty_raises_exception():
    source = ""
    with pytest.raises(ValueError):
        calculate(source)


def test_calculate_simple_addition():
    source = "+ 1 2"
    assert calculate(source) == 3
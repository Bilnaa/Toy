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


def test_calculate_div_by_zero():
    source = "/ 1 0"
    with pytest.raises(ValueError):
        calculate(source)


def test_calculate_sequence_of_operations():
    source = "* 2 / 10 5"  # (10 / 5) * 2
    assert calculate(source) == 4
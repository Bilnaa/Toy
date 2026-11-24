from dataclasses import dataclass
from typing import Any

from toy.tokens import Token


@dataclass
class Expression:
    pass

@dataclass
class Literal(Expression):
    # a literal is any literal values like (e.g True, 324, "bob")
    value: Any | None

@dataclass
class Binary(Expression):
    # a binary is a 3 + 2, 2 > 7
    left: Expression
    operator: Token
    right: Expression

@dataclass
class Unary(Expression):
    # A unary is just an operator prefixed by an operator on the right
    operator: Token
    right: Expression
#####################
# Statements
#####################

@dataclass
class Statement:
    # a statement modifies the state or the behavior of a program
    pass

@dataclass
class ExpressionStatement(Statement):
    expression: Expression

@dataclass
class VarStatement(Statement):
    name: Token
    initializer: Expression | None
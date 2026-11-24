from typing import Any

from toy.ast_nodes import Literal, Binary, Unary, ExpressionStatement, Statement, VarStatement
from toy.environment import Environment
from toy.tokens import TokenType


class Interpreter:
    def __init__(self, environment=None):
        self.environment = environment if environment is not None else Environment()

    def interpret(self, statements: list[Statement], start_index: int = 0):
        for statement in statements[start_index:]:
            self.execute(statement)

    def execute(self, stmt: Statement) -> Any:
        match stmt:
            case ExpressionStatement(expression):
                return self.evaluate(expression)
            case VarStatement(name, initializer):
                value = self.evaluate(initializer) if initializer is not None else None
                self.environment.define(name.lexeme, value)
                return value
            case _:
                raise ValueError(f"Unexpected statement: {stmt}")

    def evaluate(self, expr: Any) -> Any:
        match expr:
            case ExpressionStatement(expression):
                return self.evaluate(expression)
            case VarStatement(name, initializer):
                value = self.evaluate(initializer) if initializer is not None else None
                self.environment.define(name.lexeme, value)
                return value
            case Statement():
                return self.execute(expr)
            case Literal(value):
                return value
            case Binary(left, operator, right):
                left_value = self.evaluate(left)
                right_value = self.evaluate(right)
                match operator.type:
                    case TokenType.PLUS:
                        return left_value + right_value
                    case TokenType.MINUS:
                        return left_value - right_value
                    case TokenType.STAR:
                        return left_value * right_value
                    case TokenType.SLASH:
                        return left_value / right_value
                    case TokenType.GREATER:
                        return left_value > right_value
                    case TokenType.GREATER_EQUAL:
                        return left_value >= right_value
                    case TokenType.LESS:
                        return left_value < right_value
                    case TokenType.LESS_EQUAL:
                        return left_value <= right_value
                    case TokenType.EQUAL_EQUAL:
                        return left_value == right_value
                    case TokenType.BANG_EQUAL:
                        return left_value != right_value
                    case _:
                        raise ValueError(f"Unknown operator: {operator}")
            case Unary(operator, right):
                right_value = self.evaluate(right)
                match operator.type:
                    case TokenType.MINUS:
                        return -right_value
                    case TokenType.BANG:
                        return not right_value
                    case _:
                        raise ValueError(f"Unknown operator: {operator}")
            case _:
                raise ValueError(f"Unexpected node: {expr}")
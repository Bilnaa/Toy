from typing import Any

from toy.ast_nodes import Literal, Binary, Unary, Variable, ExpressionStatement, Statement, VarStatement, PrintStatement, \
    IfStatement, BlockStatement
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
            case PrintStatement(expr):
                value = self.evaluate(expr)
                print(value)
                return value
            case IfStatement(condition, then_branch, else_branch):
                if self.is_truthy(self.evaluate(condition)):
                    return self.execute(then_branch)
                if else_branch is not None:
                    return self.execute(else_branch)
            case BlockStatement(statements):
                return self.execute_block(statements, Environment(self.environment))
            case _:
                raise ValueError(f"Unexpected statement: {stmt}")

    def execute_block(self, statements: list[Statement], environment: Environment) -> Any:
        previous = self.environment
        self.environment = environment
        try:
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
        return None

    @staticmethod
    def is_truthy(value: Any) -> bool:
        # Only `None` and `False` are falsy (0 is truthy).
        return value is not None and value is not False

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
            case Variable(name):
                return self.environment.get(name.lexeme)
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
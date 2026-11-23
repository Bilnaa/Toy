from toy.ast_nodes import Expression
from toy.tokens import Token, TokenType


class Parser:
    def __init__(self,tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[Expression]:
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_expression())
            
        return statements

    #############################
    # Expression
    #############################

    def parse_expression(self) -> Expression:
        "will try to parse an addition or subtraction"
        left = self.parse_primary()

    def parse_primary(self) -> Expression:
        pass
    #############################
    # Utils
    #############################

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]


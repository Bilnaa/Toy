from toy.ast_nodes import Expression, Literal, Binary
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
        """will try to parse an addition or subtraction"""
        left = self.parse_factor()
        while self.match(TokenType.PLUS,TokenType.MINUS):
            operator = self.previous()
            right = self.parse_factor()
            left = Binary(left, operator, right)
        return left

    def parse_factor(self) -> Expression:
        """will try to parse a multiplication or division"""
        left = self.parse_primary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.parse_primary()
            left = Binary(left, operator, right)
        return left

    def parse_primary(self) -> Expression:
        """primary is something that we can't decompose no more like: 3, 'bob'"""
        if self.match(TokenType.NUMBER):
            return Literal(float(self.previous().lexeme))

        next_token = self.peek()
        raise SyntaxError(f"Unexpected token, token :{self.peek().lexeme}, line: {next_token.line}")

    #############################
    # Utils
    #############################

    def previous(self):
        return self.tokens[self.current - 1]

    def match(self, *types:TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self,token_type:TokenType) -> bool:
        """Check if the current token type matches the token type"""
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        """Advance the current token and return the previous token"""
        if not self.is_at_end():
            self.current += 1
        return self.previous()


    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]


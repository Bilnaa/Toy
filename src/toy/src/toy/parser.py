from typing import Callable

from toy.ast_nodes import Expression, Literal, Binary, Unary, Variable, Statement, VarStatement, ExpressionStatement, \
    PrintStatement, BlockStatement, IfStatement
from toy.tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[Statement]:
        statements: list[Statement] = []
        while not self.is_at_end():
            statements.append(self.parse_declaration())

        return statements

    #############################
    # Statement
    #############################
    def parse_declaration(self) -> Statement:
        #var a = 1;
        if self.match(TokenType.VAR):
            return self.parse_var_declaration()
        return self.parse_statement()

    def parse_var_declaration(self) -> Statement:
        # a = 1
        # |
        name = self.consume(TokenType.IDENTIFIER,"Expected variable name")
        # a = 1
        #   |
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected a ';' after variable declaration.")

        return VarStatement(name, initializer)

    def parse_statement(self) -> Statement:
        if self.match(TokenType.PRINT):
            return self.parse_print_statement()
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        if self.match(TokenType.LBRACE):
            return self.parse_block_statement()
        return self.parse_expression_statement()

    def parse_expression_statement(self) -> Statement:
        expr = self.parse_expression()
        # Allow a trailing expression without a semicolon (REPL style).
        if not self.is_at_end():
            self.consume(TokenType.SEMICOLON, "Expected a ';' after expression.")
        return ExpressionStatement(expr)

    def parse_print_statement(self) -> Statement:
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected a ';' after expression.")
        return PrintStatement(expr)

    def parse_if_statement(self) -> Statement:
        self.consume(TokenType.LPAREN, "Expected '(' after expression.")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after expression.")

        then_branch = self.parse_statement()
        else_branch = None

        if self.match(TokenType.ELSE):
            else_branch = self.parse_statement()

        return IfStatement(condition, then_branch, else_branch)

    def parse_block_statement(self) -> Statement:
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.parse_declaration())
        self.consume(TokenType.RBRACE, "Expected '}' after expression.")
        return BlockStatement(statements)






    #############################
    # Expression
    #############################

    def parse_expression(self) -> Expression:
        return self.parse_equality()

    def parse_equality(self) -> Expression:
        return self.binary_left(self.parse_comparison, [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL])

    def parse_comparison(self) -> Expression:
        return self.binary_left(self.parse_term, [TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])

    def parse_term(self) -> Expression:
        return self.binary_left(self.parse_factor, [TokenType.PLUS, TokenType.MINUS])

    def parse_factor(self) -> Expression:
        return self.binary_left(self.parse_unary, [TokenType.STAR, TokenType.SLASH])

    def parse_unary(self) -> Expression:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.parse_unary()
            return Unary(operator, right)
        return self.parse_primary()

    def parse_primary(self) -> Expression:
        """primary is something that we can't decompose no more like: 3, 'bob'"""
        if self.match(TokenType.NUMBER):
            return Literal(float(self.previous().lexeme))

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expr

        next_token = self.peek()
        raise SyntaxError(f"Unexpected token, token :{self.peek().lexeme}, line: {next_token.line}")

    #############################
    # Utils
    #############################
    def binary_left(self, operand_fn: Callable[[], Expression], operators: list[TokenType]) -> Expression:
        left = operand_fn()
        while self.match(*operators):
            operator = self.previous()
            right = operand_fn()
            left = Binary(left, operator, right)
        return left

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()

        next_token = self.peek()
        raise SyntaxError(f"{message} Got token: '{next_token.lexeme}', line: {next_token.line}")

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
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
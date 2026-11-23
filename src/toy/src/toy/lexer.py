from toy.tokens import Token, TokenType


class Lexer:
    def __init__(self, source) -> None:
        self.source = source
        self.start = 0 # start cursor
        self.current = 0 # current is going to point the "next"
        self.line = 1
        self.tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        while not  self.is_at_end():
            self.start =  self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", self.line))

        return self.tokens

    def scan_token(self) -> None:
        c = self.advance()

        match c:
            case "+":
                self.add_token(TokenType.PLUS)
            case "-":
                self.add_token(TokenType.MINUS)
            case "*":
                self.add_token(TokenType.STAR)
            case "/":
                self.add_token(TokenType.SLASH)
            case "(":
                self.add_token(TokenType.LPAREN)
            case ")":
                self.add_token(TokenType.RPAREN)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case ",":
                self.add_token(TokenType.COMMA)
            case _:
                if c.isdigit():
                    self.number()
                else:
                    raise SyntaxError(f'Unexpected character "{c}",line {self.line}')

    def add_token(self,token_type: TokenType,literal=None) -> None:
        text = self.source[self.start:self.current]
        lexeme = literal if literal is not None else text
        self.tokens.append(Token(token_type, lexeme, self.line))

    def advance(self) -> str:
        self.current += 1
        return self.current[self.current - 1]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def number(self):
        #564.93
        # Int / int part of a float (564)
        while self.peek().isdigit():
            self.advance()
        # we parse the decimal part (93)
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek_next().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER)

    def peek(self) -> str:
        """Peek at the next character without consuming it."""
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]



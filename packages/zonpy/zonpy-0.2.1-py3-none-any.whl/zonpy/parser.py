from typing import Iterator
from zonpy.lexer import Token, TokenType


class Parser:
    def __init__(self, tokens: Iterator[Token]):
        self.tokens = tokens
        self.current = None
        self.next()

    def next(self):
        try:
            self.current = next(self.tokens)
        except StopIteration:
            self.current = None

    def parse(self) -> dict | list:
        dict_result = {}
        list_result = []

        while self.current:
            if self.current.type == TokenType.LBRACE:
                self.next()

            if self.current.type == TokenType.COMMA:
                self.next()

            if self.current.type == TokenType.RBRACE:
                self.next()
                break

            if self.current.type == TokenType.IDENTIFIER:
                key = self.key()
                self.equals()
                value = self.value()

                dict_result[key] = value
            else:
                list_result.append(self.value())

        return list_result if list_result else dict_result

    def key(self):
        if self.current is not None and self.current.type == TokenType.IDENTIFIER:
            key = self.current.resolve()
            self.next()
            return key
        else:
            raise Exception(f"Expected KEY but got {self.current}")

    def value(self) -> str | int | float | bool | dict | list:
        if self.current is not None and (
            self.current.type == TokenType.STRING
            or self.current.type == TokenType.NUMBER
            or self.current.type == TokenType.BOOLEAN
        ):
            value = self.current.resolve()
            self.next()
            return value
        elif self.current is not None and self.current.type == TokenType.LBRACE:
            return self.parse()
        else:
            raise Exception(f"Expected VALUE but got {self.current}")

    def equals(self):
        if self.current is not None and self.current.type == TokenType.EQUALS:
            self.next()
        else:
            raise Exception(f"Expected EQUALS but got {self.current}")

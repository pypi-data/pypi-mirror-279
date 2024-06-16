from dataclasses import dataclass
from enum import Enum
from typing import Iterator


class TokenType(Enum):
    """Enumeration of token types."""

    IDENTIFIER = 1
    STRING = 2
    NUMBER = 3
    BOOLEAN = 4
    LBRACE = 5
    RBRACE = 6
    EQUALS = 7
    COMMA = 8


@dataclass
class Token:
    type: TokenType
    value: str

    def resolve(self):
        """Resolves the token value to its python equivalent."""
        if self.type == TokenType.STRING:
            return self.value[1:-1]
        if self.type == TokenType.NUMBER:
            return float(self.value)
        if self.type == TokenType.BOOLEAN:
            if self.value == "true":
                return True
            elif self.value == "false":
                return False
            else:
                raise ValueError("Invalid boolean value")
        if self.type == TokenType.IDENTIFIER:
            if self.value.startswith('.@"') and self.value.endswith('"'):
                return self.value[3:-1]
            return self.value[1:]
        return self.value


def read(input: str) -> Iterator[str]:
    """Reads a string and yields tokens."""
    current = ""
    previous = ""
    for c in input:
        if c.isspace():
            if current:
                print("current", current)
                yield current
                current = ""
            continue

        if c == "{":
            if previous == ".":
                current = ""
                yield ".{"
            else:
                raise ValueError("Unexpected character")
        elif c in ["}", "=", ","]:
            if current:
                yield current
            yield c
            current = ""
        else:
            current += c

        previous = c


def parse(iter: Iterator[str]) -> Iterator[Token]:
    """Parses an iterator of tokens string and returls a Token object."""
    for token in iter:
        if token == ".{":
            yield Token(TokenType.LBRACE, token)
        elif token == "}":
            yield Token(TokenType.RBRACE, token)
        elif token == "=":
            yield Token(TokenType.EQUALS, token)
        elif token == ",":
            yield Token(TokenType.COMMA, token)
        elif token.startswith('"'):
            if not token.endswith('"'):
                raise ValueError("Invalid string literal")
            yield Token(TokenType.STRING, token)
        elif token in ["true", "false"]:
            yield Token(TokenType.BOOLEAN, token)
        elif token.isdigit() or token.replace(".", "").isdigit():
            yield Token(TokenType.NUMBER, token)
        else:
            yield Token(TokenType.IDENTIFIER, token)

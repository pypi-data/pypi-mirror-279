import zonpy.lexer as lexer
import zonpy.parser


def load(file: str) -> dict:
    with open(file, "r") as f:
        return loads(f.read())


def loads(obj: str) -> dict:
    tokens = lexer.parse(lexer.read(obj))
    parser = zonpy.parser.Parser(tokens)
    return parser.parse()


def dump(file: str, obj: dict):
    raise NotImplementedError("dump() not implemented")


def dumps(obj: dict) -> str:
    result = []
    result.append(".{")

    pairs = []
    for key, value in obj.items():
        current = ""
        if "-" in key:
            key = f'@"{key}"'

        if isinstance(value, dict):
            current = f".{key} = {dumps(value)}"
        elif isinstance(value, str):
            current = f'.{key} = "{value}"'
        elif isinstance(value, bool):
            current = f".{key} = {str(value).lower()}"
        elif isinstance(value, int) or isinstance(value, float):
            current = f".{key} = {value}"

        pairs.append(current)

    result.append(", ".join(pairs))

    result.append("}")

    return "".join(result)

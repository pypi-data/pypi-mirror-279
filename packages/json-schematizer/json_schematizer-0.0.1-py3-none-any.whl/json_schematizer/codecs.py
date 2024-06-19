import orjson


def decode(s: str) -> dict:
    return orjson.loads(s)


def encode(o: dict) -> str:
    return orjson.dumps(o)

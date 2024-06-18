from typing import TypedDict


class Index(TypedDict):
    name: str
    asc: bool
    unique: bool
    expireAfterSeconds: int

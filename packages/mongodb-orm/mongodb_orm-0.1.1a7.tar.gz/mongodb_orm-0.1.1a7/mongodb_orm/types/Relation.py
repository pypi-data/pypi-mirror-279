from enum import Enum
from typing import TypedDict, Final


class RelationType(Enum):
    ONE_TO_ONE: Final[str] = "one_to_one"
    ONE_TO_MANY: Final[str] = "one_to_many"
    MANY_TO_ONE: Final[str] = "many_to_one"
    MANY_TO_MANY: Final[str] = "many_to_many"


class OnDeleteType(Enum):
    CASCADE: Final[str] = "CASCADE"
    STRICT: Final[str] = "STRICT"
    NOTHING: Final[str] = "NOTHING"


class Relation(TypedDict):
    name: str
    type: RelationType
    to_model: str
    on_delete: OnDeleteType

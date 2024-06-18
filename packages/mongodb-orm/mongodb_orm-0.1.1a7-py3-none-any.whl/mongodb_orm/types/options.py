from enum import Enum
from typing import TypedDict, Final, Optional
from mongodb_orm.types.model_schema import ModelSchema


class ValidationLevel(Enum):
    STRICT: Final[str] = "strict"
    MODERATE: Final[str] = "moderate"


class Options(TypedDict):
    schema: Optional[ModelSchema]
    validation_level: Optional[ValidationLevel]
    time_series: Optional[bool]

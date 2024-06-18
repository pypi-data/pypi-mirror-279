from enum import Enum
from typing import TypedDict, Optional, List


class Severity(Enum):
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    Warning = 'Warning'
    Info = 'Info'


class LoggerObject(TypedDict):
    severity: Severity
    what: str
    reason: str
    where: str
    traceback: Optional[List[dict] | dict | str | None]
    data: Optional[List[dict] | dict | str | None]
    consumed: bool

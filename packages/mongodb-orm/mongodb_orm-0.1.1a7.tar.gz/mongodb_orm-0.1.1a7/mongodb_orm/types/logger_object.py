from enum import Enum
from typing import TypedDict, Optional, List, Union


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
    traceback: Optional[Union[List[dict], dict, str, None]]
    data: Optional[Union[List[dict], dict, str, None]]
    consumed: bool

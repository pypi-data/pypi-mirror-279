# exception definitions
from enum import Enum, auto


# enum for gps warnings
class FixProblem(Enum):
    """enum for gps warnings"""

    NONE = auto()
    INCOMPLETE_DATA = auto()
    NO_RTK_FIX = auto()
    OLD_FIX = auto()


class FixException(Exception):
    """exception for gps fix errors"""

    def __init__(self, reason: FixProblem) -> None:
        self.reason = reason

    def __str__(self) -> str:
        return f"GPS fix problem: {self.reason.name}"

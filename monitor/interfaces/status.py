from enum import Enum


class Status(Enum):
    """Status of a task."""
    HIT_LIMIT = 0
    ERROR = 1
    SUCCESS = 2
    IN_PROGRESS = 3

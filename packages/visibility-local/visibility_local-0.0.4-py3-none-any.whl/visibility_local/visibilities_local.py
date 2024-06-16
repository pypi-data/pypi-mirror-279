from enum import Enum


class VisibilitiesLocal(Enum):
    NO_ONE = 0
    ONLY_CREATOR = 1
    EVERYONE = 2 ** 64 - 1  # Python max value != sql max value

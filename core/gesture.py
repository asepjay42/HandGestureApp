from enum import Enum, auto


class Gesture(Enum):
    """
    Seluruh mode gesture yang dikenali aplikasi.
    """

    NORMAL = auto()

    V_SIGN = auto()

    THUMBS_UP = auto()

    FIST = auto()
from collections import deque

from config import DEBOUNCE_FRAMES
from core.gesture import Gesture


class GestureDetector:
    """
    Mengubah landmark MediaPipe menjadi Gesture.
    """

    FINGER_TIPS = (8, 12, 16, 20)
    FINGER_PIPS = (6, 10, 14, 18)

    THUMB_TIP = 4
    INDEX_MCP = 5
    WRIST = 0

    def __init__(self):

        self.buffer = deque(maxlen=DEBOUNCE_FRAMES)

        self.current = Gesture.NORMAL

    # -------------------------------------------------

    @staticmethod
    def finger_up(lm, tip, pip):

        return lm[tip].y < lm[pip].y

    # -------------------------------------------------

    def get_finger_states(self, lm):

        return [
            self.finger_up(lm, tip, pip)
            for tip, pip in zip(self.FINGER_TIPS, self.FINGER_PIPS)
        ]

    # -------------------------------------------------

    def is_vsign(self, fingers):

        index, middle, ring, pinky = fingers

        return index and middle and not ring and not pinky

    # -------------------------------------------------

    def is_thumbs(self, lm, fingers):

        if any(fingers):
            return False

        hand_height = abs(
            lm[self.WRIST].y -
            lm[self.INDEX_MCP].y
        )

        if hand_height < 0.01:
            return False

        thumb_height = lm[self.INDEX_MCP].y - lm[self.THUMB_TIP].y

        return thumb_height > hand_height * 0.3

    # -------------------------------------------------

    def is_fist(self, lm, fingers):

        if any(fingers):
            return False

        hand_height = abs(
            lm[self.WRIST].y -
            lm[self.INDEX_MCP].y
        )

        if hand_height < 0.01:
            return False

        thumb_height = lm[self.INDEX_MCP].y - lm[self.THUMB_TIP].y

        return thumb_height <= hand_height * 0.3

    # -------------------------------------------------

    def debounce(self, gesture):

        self.buffer.append(gesture)

        if len(self.buffer) < DEBOUNCE_FRAMES:

            return self.current

        if all(g == gesture for g in self.buffer):

            self.current = gesture

        return self.current

    # -------------------------------------------------

    def detect(self, landmarks):

        fingers = self.get_finger_states(landmarks)

        if self.is_vsign(fingers):

            return self.debounce(Gesture.V_SIGN)

        if self.is_thumbs(landmarks, fingers):

            return self.debounce(Gesture.THUMBS_UP)

        if self.is_fist(landmarks, fingers):

            return self.debounce(Gesture.FIST)

        return self.debounce(Gesture.NORMAL)
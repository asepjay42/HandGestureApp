import cv2
import mediapipe as mp

from config import (
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    PHOTO_BLUR_MUSIC,
    JOKOWI_MUSIC,
)

from core.audio import AudioManager
from core.detector import GestureDetector
from core.gesture import Gesture
from core.renderer import Renderer

from utils.camera import Camera


class HandGestureApp:

    def __init__(self):

        # ==========================================
        # MediaPipe
        # ==========================================

        self.mp_hands = mp.solutions.hands

        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )

        # ==========================================
        # Components
        # ==========================================

        self.camera = Camera()

        self.detector = GestureDetector()

        self.renderer = Renderer()

        self.audio = AudioManager()

        # ==========================================
        # Audio
        # ==========================================

        self.audio.load(
            "blur",
            PHOTO_BLUR_MUSIC,
        )

        self.audio.load(
            "jokowi",
            JOKOWI_MUSIC,
        )

        # ==========================================
        # State
        # ==========================================

        self.mode = Gesture.NORMAL

        self.flags = {

            Gesture.THUMBS_UP: False,

            Gesture.FIST: False,

        }

        # ==========================================
        # Effect Strategy
        # ==========================================

        self.effects = {

            Gesture.V_SIGN: {

                "effect": self.renderer.render_v,

                "audio": "blur",

                "reset": self.renderer.reset_v,

            },

            Gesture.THUMBS_UP: {

                "effect": self.renderer.render_thumbs,

                "flag": Gesture.THUMBS_UP,

            },

            Gesture.FIST: {

                "effect": self.renderer.render_fist,

                "audio": "jokowi",

                "flag": Gesture.FIST,

            },

        }

    # =========================================================

    def on_mode_changed(
        self,
        new_mode,
    ):

        if new_mode == self.mode:
            return

        leaving = self.effects.get(
            self.mode
        )

        entering = self.effects.get(
            new_mode
        )

        # ======================================
        # Stop previous audio
        # ======================================

        if leaving:

            audio = leaving.get(
                "audio"
            )

            if audio:

                self.audio.stop(
                    audio
                )

        # ======================================
        # Play new audio
        # ======================================

        if entering:

            audio = entering.get(
                "audio"
            )

            if audio:

                self.audio.play(
                    audio,
                    loop=(audio == "jokowi"),
                )

            reset = entering.get(
                "reset"
            )

            if reset:

                reset()

            flag = entering.get(
                "flag"
            )

            if flag:

                self.flags[
                    flag
                ] = True

        self.mode = new_mode

    # =========================================================

    def apply_effect(
        self,
        frame,
    ):

        config = self.effects.get(
            self.mode
        )

        if not config:

            return frame

        effect = config.get(
            "effect"
        )

        flag = config.get(
            "flag"
        )

        if flag is None:

            return effect(
                frame
            )

        frame = effect(
            frame,
            self.flags[
                flag
            ],
        )

        self.flags[
            flag
        ] = False

        return frame

    # =========================================================

    def process_frame(
        self,
        frame,
    ):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        results = self.hands.process(
            rgb
        )

        detected = Gesture.NORMAL

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            detected = self.detector.detect(
                hand.landmark
            )

            if detected == Gesture.NORMAL:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(
                        color=(0, 200, 255),
                        thickness=2,
                        circle_radius=3,
                    ),
                    self.mp_draw.DrawingSpec(
                        color=(255, 255, 0),
                        thickness=2,
                    ),
                )

        self.on_mode_changed(
            detected
        )

        frame = self.apply_effect(
            frame
        )

        self.renderer.draw_status(
            frame,
            self.mode,
        )

        self.renderer.draw_hint(
            frame,
        )

        return frame

    # =========================================================

    def run(self):

        cap = self.camera.open()

        print(
            "[INFO] Hand Gesture Detection Started"
        )

        try:

            while True:

                frame = self.camera.read(
                    cap
                )

                if frame is None:

                    print(
                        "[ERROR] Failed to read frame."
                    )

                    break

                frame = self.process_frame(
                    frame
                )

                cv2.imshow(
                    "Hand Gesture Detection",
                    frame,
                )

                key = cv2.waitKey(1) & 0xFF

                if key in (
                    ord("q"),
                    ord("Q"),
                    27,
                ):
                    break

        finally:

            self.audio.stop_all()

            self.camera.release(
                cap
            )

            self.hands.close()

            print(
                "[INFO] Application Closed"
            )
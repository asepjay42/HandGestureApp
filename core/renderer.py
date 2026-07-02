import time

import cv2
import numpy as np

from config import (
    BLUR_KERNEL,
    EDGE_LOW,
    EDGE_HIGH,
    MAIN_FONT_SCALE,
    STATUS_FONT_SCALE,
    TYPEWRITER_SPEED,
    TYPEWRITER_FADE,
    FADE_DURATION,
)

from core.gesture import Gesture


class TextRenderer:

    FONT = cv2.FONT_HERSHEY_DUPLEX

    @staticmethod
    def centered(
        frame,
        text,
        scale,
        color,
        thickness=3,
        outline=(0, 0, 0),
        outline_thickness=6,
    ):

        h, w = frame.shape[:2]

        (tw, th), _ = cv2.getTextSize(
            text,
            TextRenderer.FONT,
            scale,
            thickness,
        )

        x = (w - tw) // 2
        y = (h + th) // 2

        cv2.putText(
            frame,
            text,
            (x, y),
            TextRenderer.FONT,
            scale,
            outline,
            outline_thickness,
            cv2.LINE_AA,
        )

        cv2.putText(
            frame,
            text,
            (x, y),
            TextRenderer.FONT,
            scale,
            color,
            thickness,
            cv2.LINE_AA,
        )

    @staticmethod
    def typewriter(
        frame,
        text,
        elapsed,
        scale,
        color,
        thickness=3,
        outline=(0, 0, 0),
        outline_thickness=7,
    ):

        h, w = frame.shape[:2]

        (full_width, text_height), _ = cv2.getTextSize(
            text,
            TextRenderer.FONT,
            scale,
            thickness,
        )

        base_x = (w - full_width) // 2
        base_y = (h + text_height) // 2

        progress = elapsed / TYPEWRITER_SPEED

        visible = min(int(progress) + 1, len(text))

        solid = text[: max(0, visible - 1)]

        if solid:

            cv2.putText(
                frame,
                solid,
                (base_x, base_y),
                TextRenderer.FONT,
                scale,
                outline,
                outline_thickness,
                cv2.LINE_AA,
            )

            cv2.putText(
                frame,
                solid,
                (base_x, base_y),
                TextRenderer.FONT,
                scale,
                color,
                thickness,
                cv2.LINE_AA,
            )

        if visible > len(text):
            return

        fade = text[visible - 1]

        prefix = text[: visible - 1]

        (prefix_width, _), _ = cv2.getTextSize(
            prefix,
            TextRenderer.FONT,
            scale,
            thickness,
        )

        alpha = min(
            (progress - int(progress)) / (TYPEWRITER_FADE / TYPEWRITER_SPEED),
            1.0,
        )

        fade_color = tuple(
            int(outline[i] + (color[i] - outline[i]) * alpha)
            for i in range(3)
        )

        fade_outline = tuple(
            int(outline[i] * alpha)
            for i in range(3)
        )

        x = base_x + prefix_width

        cv2.putText(
            frame,
            fade,
            (x, base_y),
            TextRenderer.FONT,
            scale,
            fade_outline,
            outline_thickness,
            cv2.LINE_AA,
        )

        cv2.putText(
            frame,
            fade,
            (x, base_y),
            TextRenderer.FONT,
            scale,
            fade_color,
            thickness,
            cv2.LINE_AA,
        )


class EffectRenderer:

    @staticmethod
    def blur(frame):

        kernel = BLUR_KERNEL

        if kernel % 2 == 0:
            kernel += 1

        return cv2.GaussianBlur(
            frame,
            (kernel, kernel),
            0,
        )

    @staticmethod
    def edge(frame):

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY,
        )

        edges = cv2.Canny(
            gray,
            EDGE_LOW,
            EDGE_HIGH,
        )

        output = np.zeros_like(frame)

        output[:, :, 0] = edges
        output[:, :, 1] = edges // 2
        output[:, :, 2] = edges

        return cv2.addWeighted(
            frame,
            0.7,
            output,
            0.8,
            0,
        )

    @staticmethod
    def overlay(
        frame,
        color,
        alpha,
    ):

        layer = np.full_like(
            frame,
            color,
        )

        return cv2.addWeighted(
            frame,
            1 - alpha,
            layer,
            alpha,
            0,
        )


class Renderer:

    STATUS = {
        Gesture.NORMAL: (
            "NORMAL MODE",
            (180, 180, 180),
        ),
        Gesture.V_SIGN: (
            "V SIGN DETECTED",
            (0, 220, 255),
        ),
        Gesture.THUMBS_UP: (
            "THUMBS UP DETECTED",
            (0, 255, 100),
        ),
        Gesture.FIST: (
            "FIST DETECTED",
            (0, 0, 255),
        ),
    }

    def __init__(self):

        self.v_start = 0.0

        self.thumb_start = 0.0

        self.fist_start = 0.0

    def reset_v(self):

        self.v_start = time.time()
    def render_v(
        self,
        frame,
    ):

        frame = EffectRenderer.blur(frame)

        TextRenderer.typewriter(
            frame,
            "Foto kita blur",
            time.time() - self.v_start,
            MAIN_FONT_SCALE,
            (255, 255, 255),
        )

        return frame

    def render_thumbs(
        self,
        frame,
        first_frame=False,
    ):

        if first_frame:
            self.thumb_start = time.time()

        frame = EffectRenderer.edge(frame)

        elapsed = time.time() - self.thumb_start

        if elapsed < FADE_DURATION:

            scale = (
                0.5
                + (MAIN_FONT_SCALE - 0.5)
                * (elapsed / FADE_DURATION)
            )

        else:

            scale = MAIN_FONT_SCALE

        TextRenderer.centered(
            frame,
            "Mantap!",
            scale,
            (0, 255, 200),
            thickness=3,
            outline=(0, 0, 0),
            outline_thickness=7,
        )

        return frame

    def render_fist(
        self,
        frame,
        first_frame=False,
    ):

        if first_frame:
            self.fist_start = time.time()

        frame = EffectRenderer.overlay(
            frame,
            (0, 0, 180),
            0.30,
        )

        elapsed = time.time() - self.fist_start

        if elapsed < 0.15:

            progress = elapsed / 0.15

            scale = (
                0.3
                + (MAIN_FONT_SCALE + 0.5 - 0.3)
                * progress
            )

        elif elapsed < 0.30:

            progress = (elapsed - 0.15) / 0.15

            scale = (
                MAIN_FONT_SCALE + 0.5
                - 0.5 * progress
            )

        else:

            scale = MAIN_FONT_SCALE

        TextRenderer.centered(
            frame,
            "Hidup Jokowi!!!",
            scale,
            (0, 0, 255),
            thickness=4,
            outline=(255, 255, 255),
            outline_thickness=8,
        )

        return frame

    def draw_status(
        self,
        frame,
        mode,
    ):

        label, color = self.STATUS.get(
            mode,
            (
                "UNKNOWN",
                (255, 255, 255),
            ),
        )

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (340, 36),
            (0, 0, 0),
            -1,
        )

        cv2.addWeighted(
            overlay,
            0.5,
            frame,
            0.5,
            0,
            frame,
        )

        cv2.putText(
            frame,
            label,
            (10, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            STATUS_FONT_SCALE,
            color,
            2,
            cv2.LINE_AA,
        )

    @staticmethod
    def draw_hint(frame):

        h, w = frame.shape[:2]

        hint = "Q / ESC : Exit"

        (tw, _), _ = cv2.getTextSize(
            hint,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            1,
        )

        cv2.putText(
            frame,
            hint,
            (w - tw - 10, h - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (170, 170, 170),
            1,
            cv2.LINE_AA,
        )
import cv2


class HUD:
    """
    Head-Up Display (HUD)

    Bertugas menampilkan informasi aplikasi
    seperti FPS, Gesture, Camera Status, dsb.
    """

    def __init__(self):

        self.margin = 15

        self.width = 250

        self.height = 80

        self.alpha = 0.35

    # =====================================================

    def draw(
    self,
    frame,
    data,
    ):
        fps = data.get("fps", 0)

        gesture = data.get("gesture", None)

        gesture_text = gesture.name if gesture else "-"

        gesture_color = self.get_gesture_color(
            gesture
        )

        fps_color = self.get_fps_color(
            fps
        )

        overlay = frame.copy()

        x = self.margin

        y = self.margin

        # ---------------------------------------
        # Background Panel
        # ---------------------------------------

        cv2.rectangle(
            overlay,
            (x, y),
            (x + self.width, y + self.height),
            (25, 25, 25),
            -1,
        )

        cv2.addWeighted(
            overlay,
            self.alpha,
            frame,
            1 - self.alpha,
            0,
            frame,
        )

        # ---------------------------------------
        # FPS
        # ---------------------------------------

        fps_text = f"FPS : {fps}"

        cv2.putText(
            frame,
            fps_text,
            (x + 12, y + 28),
            cv2.FONT_HERSHEY_DUPLEX,
            0.65,
            fps_color,
            2,
            cv2.LINE_AA,
        )

        # ---------------------------------------
        # Gesture
        # ---------------------------------------

        gesture_text = (
            gesture.name
            if gesture else "-"
        )

        cv2.putText(
            frame,
            f"Gesture : {gesture_text}",
            (x + 12, y + 60),
            cv2.FONT_HERSHEY_DUPLEX,
            0.60,
            gesture_color,
            2,
            cv2.LINE_AA,
        )

    # =====================================================

    def get_gesture_color(self, gesture):

        colors = {
            "NORMAL": (80, 80, 80),
            "V_SIGN": (255, 120, 0),
            "THUMBS_UP": (0, 180, 0),
            "FIST": (0, 0, 220),
        }

        if gesture is None:
            return (80, 80, 80)

        return colors.get(
            gesture.name,
            (80, 80, 80),
        )

    # =====================================================

    def get_fps_color(self, fps):

        if fps >= 25:
            return (0, 220, 0)

        if fps >= 15:
            return (0, 220, 220)

        return (0, 0, 255)
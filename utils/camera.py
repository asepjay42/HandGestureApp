import subprocess

import cv2

from config import (
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_FPS,
)


class Camera:
    """
    Camera Manager

    Mencari kamera fisik secara otomatis,
    mengabaikan kamera virtual seperti DroidCam.
    """

    SKIP_CAMERAS = [
        "droidcam",
        "obs",
        "manycam",
        "snap camera",
    ]

    def __init__(self):

        self.index = self.find_camera()

    # ---------------------------------------------------------

    @staticmethod
    def get_camera_names():

        try:

            cmd = (
                'powershell -Command '
                '"Get-PnpDevice -Class Camera -Status OK '
                '| Select-Object -ExpandProperty FriendlyName"'
            )

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5,
                shell=True,
            )

            return [
                name.strip()
                for name in result.stdout.splitlines()
                if name.strip()
            ]

        except Exception:

            return []

    # ---------------------------------------------------------

    def find_camera(self):

        names = self.get_camera_names()

        if names:

            print(f"[INFO] Camera Found : {names}")

            for index, name in enumerate(names):

                if not any(
                    skip in name.lower()
                    for skip in self.SKIP_CAMERAS
                ):

                    print(
                        f"[INFO] Using Camera : {name}"
                    )

                    return index

        print("[INFO] Using Default Camera (0)")

        return 0

    # ---------------------------------------------------------

    def open(self):

        cap = cv2.VideoCapture(
            self.index,
            cv2.CAP_DSHOW,
        )

        if not cap.isOpened():

            cap = cv2.VideoCapture(
                self.index
            )

        if not cap.isOpened():

            raise RuntimeError(
                "Cannot open webcam."
            )

        cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH,
        )

        cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT,
        )

        cap.set(
            cv2.CAP_PROP_FPS,
            CAMERA_FPS,
        )

        return cap

    # ---------------------------------------------------------

    @staticmethod
    def read(cap):

        success, frame = cap.read()

        if not success:

            return None

        return cv2.flip(
            frame,
            1,
        )

    # ---------------------------------------------------------

    @staticmethod
    def release(cap):

        if cap:

            cap.release()

        cv2.destroyAllWindows()
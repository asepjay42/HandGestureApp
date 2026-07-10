from collections import deque
import time


class FPSCounter:

    def __init__(
        self,
        history=10,
        refresh_interval=0.5,
    ):

        self.prev_time = time.perf_counter()

        self.history = deque(maxlen=history)

        self.refresh_interval = refresh_interval

        self.last_refresh = self.prev_time

        self.display_fps = 0

    # ======================================================

    def update(self):

        current = time.perf_counter()

        delta = current - self.prev_time

        self.prev_time = current

        if delta <= 0:
            return self.display_fps

        fps = 1.0 / delta

        self.history.append(fps)

        # Update angka HUD hanya setiap refresh_interval detik
        if current - self.last_refresh >= self.refresh_interval:

            average = sum(self.history) / len(self.history)

            self.display_fps = round(average)

            self.last_refresh = current

        return self.display_fps
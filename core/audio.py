import pygame


class AudioManager:
    """
    Mengelola seluruh audio aplikasi.
    """

    def __init__(self):

        self.enabled = False
        self.sounds = {}
        self.channels = {}

        try:

            pygame.mixer.init()

            self.enabled = True

        except Exception as e:

            print(f"Audio disabled : {e}")

    def load(self, name, path):

        if not self.enabled:
            return

        self.sounds[name] = pygame.mixer.Sound(str(path))

    def play(self, name, loop=True):

        if not self.enabled:
            return

        if name not in self.sounds:
            return

        channel = self.channels.get(name)

        if channel and channel.get_busy():
            return

        self.channels[name] = self.sounds[name].play(-1 if loop else 0)

    def stop(self, name):

        if not self.enabled:
            return

        channel = self.channels.get(name)

        if channel and channel.get_busy():

            channel.stop()

    def stop_all(self):

        if not self.enabled:
            return

        pygame.mixer.stop()
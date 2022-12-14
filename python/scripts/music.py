import pygame

class Music():
    def __init__(self):
        pygame.mixer.init()
        self.song = None

    def play(self, path):
        self.song = pygame.mixer.Sound(path)
        self.song.play()

    def pause(self):
        self.song.pause()
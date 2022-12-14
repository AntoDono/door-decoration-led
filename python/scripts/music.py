import pygame

class Music():
    def __init__(self):
        pygame.mixer.init()
        self.song = None

    def play(filepath):
        self.song = pygame.mixer.Sound(filepath)
        self.song.play()

    def pause():
        self.song.pause()
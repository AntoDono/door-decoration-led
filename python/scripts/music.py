import pygame

class Music():
    def __init__(self):
        pygame.mixer.init()
        pygame.init() #turn all of pygame on.
        self.song = None

    def play(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()
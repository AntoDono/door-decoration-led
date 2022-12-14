import pygame

class Music():
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
        pygame.init() #turn all of pygame on.
        self.song = None

    def play(self, path):
        self.song = pygame.mixer.Sound(path)
        self.song.play()

    def pause(self):
        self.song.pause()
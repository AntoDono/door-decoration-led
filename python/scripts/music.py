import pygame

class Music():
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        self.song = None

    def play(self, path):
        self.song = pygame.mixer.Sound(path)
        self.song.play()
        print("Done playing")

    def pause(self):
        self.song.pause()
#!/usr/bin/env python
# from gifViewer import GifViewer
from music import Music
import os.path as path
import pygame

# music = Music()
# music.play("Merry_Christmas.wav")
# print(path.abspath(path.join(__file__, "../../../assets/mp3/Merry_Christmas.mp3")))

pygame.mixer.init()
crash_sound = pygame.mixer.Sound("Merry_Christmas.wav")
crash_sound.play()


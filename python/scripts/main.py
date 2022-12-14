#!/usr/bin/env python
from gifViewer import GifViewer
from music import Music
import os.path as path

music = Music()
print(path.abspath(path.join(__file__, "../../assets/mp3/Merry_Christmas.mp4")))
music.play(path.abspath(path.join(__file__, "../../assets/mp3/Merry_Christmas.mp4")))
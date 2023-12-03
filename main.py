import pygame as pg
import random
import os
from pygame.time import Clock, get_ticks
import tkinter as tk
from tkinter import messagebox

from settings import *


# Constantes
CUR_PATH = os.path.dirname(__file__)

KEYS = ["A","B","C","D","E","F","G","H","I","J",
"K","L","M","N","O","P","Q","R","S","T",
"U","V","W","X","Y","Z"]

class Game():
    def __init__(self):
        x = 0
    
    def run(self):
        # Boucle du jeu
        self.playing = True
        while self.playing:
            self.tick = pg.time.get_ticks()
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()
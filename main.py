import pygame as pg
import pymunk as pm
from pymunk.pygame_util import DrawOptions
import random
import os
#RIP Clock
import tkinter as tk
from tkinter import messagebox
from sprites import * 
from settings import *


# Constantes
CUR_PATH = os.path.dirname(__file__)

KEYS = ["A","B","C","D","E","F","G","H","I","J",
"K","L","M","N","O","P","Q","R","S","T",
"U","V","W","X","Y","Z"]

background = (236, 186, 0)


class Game():
    def __init__(self):
        self.running = True
    
    def run(self):
        # Boucle du jeu
        self.playing = True
        while self.playing:
            self.tick = pg.time.get_ticks()
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()

    def new(self):
        pg.init()
        pg.display.set_caption("Melon")

        self.space = pm.Space()
        self.space.gravity = (0, 900)


        self.calibri_font = pg.font.SysFont("Calibri", 25)
        self.clock = pg.time.Clock()
        self.screenGame = pg.display.set_mode((480, 600))
        self.draw_options = DrawOptions(self.screenGame)

        self.ground = Sol(self.space)
        self.space.add(self.ground.ground)

        self.mur1 = Mur(100, self.space)
        self.space.add(self.mur1.wall)
        self.mur2 = Mur(380, self.space)
        self.space.add(self.mur2.wall)

        self.all_Fruits = pg.sprite.Group()

        for x in range(7):
            self.all_Fruits.add(Fruits(random.randint(150, 330), random.randint(0, 300), random.randint(10, 50), "joe"))

        for fruit in self.all_Fruits:
            self.space.add(fruit.circle_body, fruit.circle_shape)

        self.run()
        pg.quit()
    
    def event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    #self.running = False
                    self.playing = False
            elif event.type == pg.QUIT:
                self.running = False
                self.playing = False
                
    def update(self):
        self.space.step(1 / 60.0)

    def draw(self):
        self.screenGame.fill(background)
        self.space.debug_draw(self.draw_options)

        for fruit in self.all_Fruits:
            fruit.draw(self.screenGame)

        pg.display.flip()
    
    def show_start_screen(self):
        pass

g = Game()

g.new()
while g.running:
    g.new()
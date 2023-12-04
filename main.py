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

        self.all_sprites = pg.sprite.Group()
        self.all_Fruits = pg.sprite.Group()

        self.ground = Sol(self.space)
        self.space.add(self.ground.ground)

        self.mur1 = Mur(100, self.space)
        self.space.add(self.mur1.wall)
        self.mur2 = Mur(380, self.space)
        self.space.add(self.mur2.wall)

        self.collideLine = CollideLine((240, 200))
        self.all_sprites.add(self.collideLine)
        self.viseLine = ViseLine((240, 0))
        self.all_sprites.add(self.viseLine)


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
            
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pg.mouse.get_pos()
                    new_fruit = Fruits(pos[0], 100, random.randint(10, 50), "joe")
                    self.all_Fruits.add(new_fruit)
                    self.space.add(new_fruit.circle_body, new_fruit.circle_shape)
                
    def update(self):
        self.space.step(1 / 60.0)

        self.viseLine.update(pg.mouse.get_pos())

        for fruit in self.all_Fruits:
            if fruit.circle_body.position.y > 600 or fruit.circle_body.position.y < -100:
                self.all_Fruits.remove(fruit)
                self.space.remove(fruit.circle_body, fruit.circle_shape)
            
            if pg.sprite.collide_rect(self.collideLine, fruit):
                print(fruit.circle_body.velocity.y)
                if abs(fruit.circle_body.velocity.y) < 1e-3:
                    self.playing = False

    def draw(self):
        self.screenGame.fill(background)
        self.space.debug_draw(self.draw_options)

        self.all_sprites.draw(self.screenGame)

        for fruit in self.all_Fruits:
            fruit.draw(self.screenGame)

        pg.display.flip()
    
    def show_start_screen(self):
        pass

g = Game()

g.new()
while g.running:
    g.new()
import pygame as pg
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


        self.calibri_font = pg.font.SysFont("Calibri", 25)
        self.clock = pg.time.Clock()
        self.screenGame = pg.display.set_mode((480, 600))

        self.Fruit1 = Fruits()
        self.all_Fruits = pg.sprite.Group()
        self.all_Fruits.add(self.Fruit1)

        self.all_deco = pg.sprite.Group()
        self.all_deco.add(Sol())


        self.run()
        pg.quit()
    
    def event(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    self.playing = False
            elif event.type == pg.QUIT:
                self.running = False
                self.playing = False
                
    
    def update(self):
        for Fruit in self.all_Fruits:
            Fruit.update()
        
        

    def draw(self):
        self.screenGame.fill(background)
        self.all_Fruits.draw(self.screenGame)
        self.all_deco.draw(self.screenGame)

    


        pg.display.flip()
    



g = Game()

g.new()
while g.running :
    g.new()
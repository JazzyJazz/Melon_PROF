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
        self.viseLine = ViseLine((240, 300))
        self.all_sprites.add(self.viseLine)

        self.cooldown = False
        
        self.Profs = ["Domon","Redon","Mueller","Keller", "Dubail","Gaillard","Mischler","Tharin","Wiser"]
        self.dicoProfs = {"Redon": 10,"Domon":15,"Mischler": 50,"Tharin": 45,"Keller":25,"Gaillard":35,"Dubail":40,"Mueller":20,"Wiser":30}
        self.dicoRadius = {10:"Redon", 15:"Domon", 50:"Mischler", 45:"Tharin", 25:"Keller", 35:"Gaillard", 40:"Dubail", 20:"Mueller", 30:"Wiser"}
        self.nom = random.choice(self.Profs[0:4])

        next_fruit = Fruits(240, 100, self.dicoProfs[self.nom], self.nom)
        self.all_sprites.add(next_fruit)
        #RIP Andrea Pfammater Tavel et Phillipe Pittet



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
                if event.button == 1 and not self.cooldown:
                    pos = pg.mouse.get_pos()
                    if not pg.mouse.get_pos()[0] > 100:
                        pos = (101, 100)
                    elif not pg.mouse.get_pos()[0] < 380:
                        pos = (379, 100)
                    self.all_sprites.remove(self.all_sprites.sprites()[-1])
                    new_fruit = Fruits(pos[0], 100, self.dicoProfs[self.nom], self.nom)
                    self.all_Fruits.add(new_fruit)
                    self.space.add(new_fruit.circle_body, new_fruit.circle_shape)
                    self.cooldown = True
                    self.cooldown_time = pg.time.get_ticks()

                    self.nom = random.choice(self.Profs[0:4])
                    next_fruit = Fruits(pos[0], 100, self.dicoProfs[self.nom], self.nom)
                    self.all_sprites.add(next_fruit)
                
    def update(self):
        self.space.step(1 / 60.0)

        if pg.mouse.get_pos()[0] > 100 and pg.mouse.get_pos()[0] < 380:
            self.viseLine.update(pg.mouse.get_pos())
            self.all_sprites.sprites()[-1].rect.center = (pg.mouse.get_pos()[0], 100)

        if self.cooldown:
            if self.tick - self.cooldown_time > 1000:
                self.cooldown = False

        for fruit in self.all_Fruits:
            if fruit.circle_body.position.y > 600 or fruit.circle_body.position.y < -100:
                self.all_Fruits.remove(fruit)
                self.space.remove(fruit.circle_body, fruit.circle_shape)
            
            if fruit.rect.center[1] < 160:
                if abs(fruit.circle_body.velocity.y) < 1e-2:
                    self.playing = False

            if pg.sprite.spritecollide(fruit, self.all_Fruits, False):
                collided = False
                for fruit2 in pg.sprite.spritecollide(fruit, self.all_Fruits, False):
                    if fruit2 != fruit and not collided and (fruit2.circle_body in self.space.bodies and fruit.circle_body in self.space.bodies):
                        if fruit2.nom == fruit.nom and fruit.nom != "Mischler":
                            mid_point = ((fruit.rect.center[0] + fruit2.rect.center[0]) / 2, (fruit.rect.center[1] + fruit2.rect.center[1]) / 2)
                            new_fruit = Fruits(mid_point[0], mid_point[1], fruit.radius+5, self.dicoRadius[fruit.radius+5])
                            self.all_Fruits.add(new_fruit)
                            self.space.add(new_fruit.circle_body, new_fruit.circle_shape)
                            self.all_Fruits.remove(fruit)
                            self.space.remove(fruit.circle_body, fruit.circle_shape)
                            self.all_Fruits.remove(fruit2)
                            self.space.remove(fruit2.circle_body, fruit2.circle_shape)
                            collided = True
                            break

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
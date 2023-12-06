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
backgroundHEX = "#ecba00"


class Game():
    def __init__(self):
        self.running = True
        self.score = 1
    
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
        self.screengame = pg.display.set_mode((480, 600))
        self.draw_options = DrawOptions(self.screengame)
        pg.display.set_caption("Melon")

        self.space = pm.Space()
        self.space.gravity = (0, 900)


        self.calibri_font = pg.font.SysFont("Calibri", 25)
        self.clock = pg.time.Clock()
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

        self.score = 0
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
                            self.score += int((fruit.radius/10)**2)
                            break

    def draw(self):
        self.screengame.fill(background)
        self.space.debug_draw(self.draw_options)

        self.all_sprites.draw(self.screengame)

        for fruit in self.all_Fruits:
            fruit.draw(self.screengame)

        pg.display.flip()
    
    def show_start_screen(self, start_or_restart):    
        self.isTkclosed = False

        self.startScreen = tk.Tk()
        self.startScreen.title("MELON! Edition GYMNASE DE BEAULIEU 2023")
        self.startScreen.resizable(False, False)  # This code helps to disable windows from resizing

        window_height = 500
        window_width = 900

        screen_width = self.startScreen.winfo_screenwidth()
        screen_height = self.startScreen.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.startScreen.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        
        self.startScreen.config(bg=backgroundHEX)
        
        def on_closing():
            if messagebox.askokcancel("Quit", "Voulez-vous quitter?"):
                self.startScreen.destroy()
                self.isTkclosed = True
                g.running = False

        def startGame():
            self.startScreen.destroy()
            self.new()

        self.titleFrame = tk.Frame(self.startScreen, bg=backgroundHEX)
        self.titleFrame.pack()
        self.title = tk.Label(self.titleFrame, text="PASTEQUE LE JEU!", bg=backgroundHEX, fg="black")
        self.title.config(font=("Consola", 60, ))
        self.title.pack()


        self.recoreFrame = tk.Frame(self.startScreen, bg=backgroundHEX, pady=20)
        self.recoreFrame.pack()

        if start_or_restart == "Restart":
            self.scoreLabel = tk.Label(self.recoreFrame, text = "Score : " + str(self.score), bg=backgroundHEX, fg="black")
            self.scoreLabel.config(font=("Consola", 20))
            self.scoreLabel.pack()
        else:
            pass
        
        with open("record.txt", "r") as f:
            xrecord = f.read()
            xrecord = int(xrecord)
        self.recoreLabel = tk.Label(self.recoreFrame, text = "Best Score : " + str(xrecord), bg=backgroundHEX, fg="black")
        self.recoreLabel.config(font=("Consola", 20))
        self.recoreLabel.pack()

        self.startButtonFrame = tk.Frame(self.startScreen, pady=10, bg=backgroundHEX)
        self.startButtonFrame.pack()
        self.startButton = tk.Button(self.startButtonFrame, text=start_or_restart, width= 15, height = 2, bg=backgroundHEX, command=startGame, fg="black")
        self.startButton.config(font=("Consola", 20))
        self.startButton.pack()
        

        self.startScreen.protocol("WM_DELETE_WINDOW", on_closing)

        self.startScreen.mainloop()
        return


g = Game()

start_or_restart = "Start"
show_start_screen_value = g.show_start_screen(start_or_restart)
while g.running:
    if g.score > int(open("record.txt", "r").read()):
        with open("record.txt", "w") as f:
            f.write(str(g.score))
    if start_or_restart == "Start":
        if g.score == 0:
            break
            
    show_start_screen_value = g.show_start_screen("Restart") 

pg.quit()
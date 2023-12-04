from typing import Any
import pygame as pg
import pymunk as pm
vec = pg.Vector2
import random
import os

CUR_PATH = os.path.dirname(__file__)

class Fruits(pg.sprite.Sprite):
    def __init__(self, x, y, radius, nom):
        super().__init__()
        self.image = pg.image.load(os.path.join(CUR_PATH, "Images", nom + ".png")).convert_alpha()
        self.image = pg.transform.scale(self.image, (radius*2, radius*2))
        self.circle_body = pm.Body(radius**2, 1000)
        self.circle_body.position = (x, y)
        self.circle_shape = pm.Circle(self.circle_body, radius)
    
    def draw(self, screen):
        circle_position = int(self.circle_body.position.x - self.image.get_width() / 2), int(self.circle_body.position.y - self.image.get_height() / 2)
        screen.blit(self.image, circle_position)

class Sol(pg.sprite.Sprite):
    def __init__(self, space):
        super().__init__()
        self.ground = pm.Segment(space.static_body, (0, 600), (480, 600), 5)
        self.ground.friction = 1

class Mur(pg.sprite.Sprite):
    def __init__(self, pos, space):
        super().__init__()
        self.wall = pm.Segment(space.static_body, (pos, 200), (pos, 600), 4)
        self.wall.friction = 1
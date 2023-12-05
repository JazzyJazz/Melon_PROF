from typing import Any
import pygame as pg
import pymunk as pm
vec = pg.Vector2
import random
import os

# Constantes
CUR_PATH = os.path.dirname(__file__)

class Fruits(pg.sprite.Sprite):
    def __init__(self, x, y, radius, nom):
        super().__init__()
        self.image = pg.image.load(os.path.join(CUR_PATH, "Images", nom + ".png")).convert_alpha()
        self.image = pg.transform.scale(self.image, (radius*2, radius*2))
        self.circle_body = pm.Body(radius**2, 10)
        self.circle_body.position = (x, y)
        self.circle_shape = pm.Circle(self.circle_body, radius)
        self.circle_shape.friction = 1
        self.rect = self.image.get_rect()
    
    def draw(self, screen):
        self.rect.center = int(self.circle_body.position.x - self.image.get_width() / 2), int(self.circle_body.position.y - self.image.get_height() / 2)
        rotated_image = pg.transform.rotate(self.image, -self.circle_body.angle * 180 / 3.14)
        rotated_rect = rotated_image.get_rect(center=(self.circle_body.position.x, self.circle_body.position.y))
        screen.blit(rotated_image, rotated_rect.topleft)

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

class ViseLine(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((4, 500))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    def update(self, pos):
        self.rect.center = (pos[0], 350)

class CollideLine(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((280, 2))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos
from typing import Any
import pygame as pg
vec = pg.Vector2
import random
import os

class Fruits(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.pos = vec(240, 450)
        self.vitesse = vec(0, 0)
        self.rect.midbottom = self.pos


    def update(self):
        g = vec(0, 0.3)
        self.vitesse.y += g.y
        self.pos += 0.5 * g + self.vitesse
        self.rect.midbottom = self.pos

class Sol(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((480, 50))
        self.image.fill((140, 100, 0))
        self.rect = self.image.get_rect()
        self.pos = vec(240, 600)
        self.rect.midbottom = self.pos
# Sprite classes for PyGame
import pygame as pg
from Configs import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # Jump only if standing in platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:

            self.vel.y = -20

    def update(self):
        self.acc = vec(0, GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        elif keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        # Friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # Equações de movimento
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pg.sprite.Sprite):

    global ENEMY_ACC

    def __init__(self, x, y, x_end):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (x, y)
        self.vel = vec(0, 0)
        self.end = x_end
        self.start = x
        
            
    def update(self):

        if self.vel.x >= 0 and self.rect.x < self.end:
            self.vel.x = 1
        elif self.rect.x == self.end:
            self.vel.x = -1
        elif self.vel.x < 0 and self.rect.x > self.start:
            self.vel.x = -1
        elif self.rect.x == self.start:
            self.vel.x = 1

        self.pos += self.vel

        self.rect.midbottom = self.pos





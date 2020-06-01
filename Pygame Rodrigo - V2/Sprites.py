# Sprite classes for PyGame
import pygame as pg
from Configs import *
import math
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

    def __init__(self, game, x, y, distance):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.walk_frames_r[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (x, y)
        self.vel = vec(0, 0)
        self.end = x + distance
        self.start = x
        
    def update(self):

        self.animate()
        if self.vel.x >= 0 and self.rect.x < self.end:
            self.vel.x = 0.8
        elif self.rect.x == self.end:
            self.vel.x = -0.8
        elif self.vel.x < 0 and self.rect.x > self.start:
            self.vel.x = -0.8
        elif self.rect.x == self.start:
            self.vel.x = 0.8

        self.pos += self.vel

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.x !=  0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 175:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]

        if not self.walking:
            if now - self.last_update > 300:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]


    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(112, 19, 16, 13), #0
                                self.game.spritesheet.get_image(112, 19, 16, 13),
                                self.game.spritesheet.get_image(112, 19, 16, 13),
                                self.game.spritesheet.get_image(128, 19, 16, 13)] #1

        self.walk_frames_l = [self.game.spritesheet.get_image(112, 35, 14, 13),  #2
                              self.game.spritesheet.get_image(129, 35, 14, 13),  #3
                              self.game.spritesheet.get_image(145, 35, 16, 13),  #4
                              self.game.spritesheet.get_image(160, 35, 16, 13),  #5
                              self.game.spritesheet.get_image(176, 35, 16, 13),  #6
                              self.game.spritesheet.get_image(192, 35, 16, 13)]  #7

        self.walk_frames_r = []

        for frame in self.walk_frames_l:
            self.walk_frames_r.append(pg.transform.flip(frame, True, False))


class Spritesheet():

    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, heigth):
        image = pg.Surface((width, heigth))
        image.blit(self.spritesheet, (0,0), (x, y, width, heigth))
        image = pg.transform.scale(image, (width * 3, heigth * 3))
        return image


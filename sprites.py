import pygame
import os
from Configurações import *
vec = pygame.math.Vector2

#Configurando pasta e Assets(Figura que vai ser o player)
pasta = os.path.dirname(__file__)
imagem1 = os.path.join(pasta, "Tiles")

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA/2, ALTURA/2)
        self.pos = vec(LARGURA/2, ALTURA/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20
        
    def update(self):
        
        self.acc = vec(0,GRAVIDADE)
        self.vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        self.acc.x += self.vel.x * PLAYER_FRICTION            
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.rect.midbottom =  self.pos
        
        if self.pos.x >= 1000:
            self.pos.x = 1000
        if self.pos.x < 0:
            self.pos.x = 0
        
class Platforms(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(imagem1, "grassMid.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = ALTURA-120
        
class Platforms2(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(imagem1, "grassCenter.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = ALTURA-80
        
class Platforms3(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(imagem1, "grassCenter.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = ALTURA-40
        
        

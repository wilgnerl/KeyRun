# Platform game

import pygame as pg
import random
import math
from Configs import *
from Sprites import *
from os import path

class Game:

    global FPS

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET_ENEMY))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemys = pg.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.e = Enemy(self, 350, HEIGHT - 40, 200)
        self.all_sprites.add(self.e)
        self.enemys.add(self.e)

        self.e2 = Enemy(self, 600, HEIGHT - 40, 100)
        self.all_sprites.add(self.e2)
        self.enemys.add(self.e2)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        #Inputs (Events)
        for event in pg.event.get():
        
            #Fechar a janela
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

                self.running = False

    def update(self):

        global FPS

        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        if self.e.vel.y > 0:
            hits = pg.sprite.groupcollide(self.enemys, self.platforms, False, False)
            if hits:
                self.e.pos.y = hits[0].rect.top
                self.e.vel.y = 0

        for enemy in self.enemys:
            if g.proximidade(self.player, enemy, 100):
                FPS = 10
            



    def draw(self):
        #Draw / render
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)  # Desenha os sprites
        # Depois de desenhar tudo!
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def proximidade(self, objeto1, objeto2, distancia):
        return math.hypot(objeto2.pos.x - objeto1.pos.x, objeto2.pos.y - objeto1.pos.y) < float(distancia)


g = Game()
g.show_start_screen()


while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
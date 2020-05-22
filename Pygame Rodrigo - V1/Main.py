# Platform game

import pygame as pg
import random
from Configs import *
from Sprites import *

class Game:

    global ENEMY_ACC

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

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

        self.e = Enemy(350, HEIGHT - 40, 500)
        self.all_sprites.add(self.e)
        self.enemys.add(self.e)

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

        global ENEMY_ACC

        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        if self.e.vel.y > 0:
            hits = pg.sprite.spritecollide(self.e, self.platforms, False)
            if hits:
                self.e.pos.y = hits[0].rect.top
                self.e.vel.y = 0


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

g = Game()
g.show_start_screen()


while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
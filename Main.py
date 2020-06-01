import pygame
import random
from Configurações import *
from sprites import *

class Game:
    
    def __init__(self):
        #Inicia a tela
        #Iniciando Pygame
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.running = True
    
    def new(self):
        #Inicia o jogo
        self.todas_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.todas_sprites.add(self.player)
        for i in range(0,5000, TILE_SIZE):
            p1 = Platforms(i)
            self.platforms.add(p1)
            self.todas_sprites.add(p1)
        
        for i in range(0,5000, TILE_SIZE):
            p1 = Platforms2(i)
            self.platforms.add(p1)
            self.todas_sprites.add(p1)
            
        for i in range(0,5000, TILE_SIZE):
            p1 = Platforms3(i)
            self.platforms.add(p1)
            self.todas_sprites.add(p1)
        
        self.run()
     
    def run(self):
        #Inicia Loop
        self.playing = True
        while self.playing:
            
             self.clock.tick(FPS)
             self.events()
             self.update()
             self.draw()
    
    def update(self):
        #Atualiza o loop
        self.todas_sprites.update()
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top 
                self.player.vel.y = 0 
                
        if self.player.rect.right > LARGURA/2:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
        
        '''if self.player.rect.right < LARGURA/2:         
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)'''
           
    def events(self):
        #Eventos do loop
        eventos = pygame.event.get()
        for eventos in eventos:
            if eventos.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
            self.running = False

            if eventos.type == pygame.KEYDOWN:
                if eventos.key == pygame.K_SPACE:
                    self.player.jump()
                     
    def draw(self):
        #Desenha as imagens
        self.tela.fill(GREEN2)
   
        self.todas_sprites.draw(self.tela)
        
        #Sempre que desenhar use isso
        pygame.display.flip()
    
    def show_start_screen(self):
        pass
    
    def show_go_screen(self):
        pass
            
g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()
    
pygame.quit() 
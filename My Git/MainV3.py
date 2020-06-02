import pygame
import random
from Configurações import *
from spritesv2 import *


class Game:
    
    def __init__(self):
        #Inicia a tela
        #Iniciando Pygame
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()
    
    def load_data(self):
        self.dir = os.path.dirname(__file__)
        img_dir = os.path.join(self.dir, 'Tiles')
        self.spritesheet_enemy = Spritesheet(os.path.join(img_dir,SPRITESHEET_ENEMY))
    
    def new(self):
        #Inicia o jogo
        self.todas_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
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
            
        self.e = Enemy(self, 350, ALTURA - 40, 200)
        self.todas_sprites.add(self.e)
        self.enemys.add(self.e)

        
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
        
        for enemy in self.enemys:        
            if enemy.vel.y > 0:
                hits = pygame.sprite.spritecollide(enemy, self.platforms, False)
                if hits:
                    enemy.pos.y = hits[0].rect.top
                    enemy.vel.y = 0
        
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
        
        self.tela.fill(BLUE)
        self.draw_text(TITLE, 48, WHITE, LARGURA/2, ALTURA/4)
        self.draw_text("Start", 22, WHITE, LARGURA/2, ALTURA/2)
        self.draw_text("Quit", 22, WHITE, LARGURA/2, 500)
        pygame.display.flip()
        self.wait_for_key()
        
    def show_go_screen(self):
        
        pass
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                
                if event.type == pygame.KEYUP:
                    waiting = False
           
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.tela.blit(text_surface, text_rect)
                
g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()
    
pygame.quit() 
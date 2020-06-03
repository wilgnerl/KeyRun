import pygame
import random, math
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
        self.end_time = 0
        self.bool_contato = False
    
    def load_data(self):
        self.dir = os.path.dirname(__file__)
        img_dir = os.path.join(self.dir, 'Tiles')
        self.spritesheet_enemy = Spritesheet(os.path.join(img_dir, SPRITESHEET_ENEMY))
        self.spritesheet_keys = Spritesheet(os.path.join(img_dir, SPRITESHEE_KEYS))
    
    def new(self):
        #Inicia o jogo
        self.todas_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.player = Player(self)
        self.todas_sprites.add(self.player)
        self.grupo_setas = pygame.sprite.Group()
        
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
            
        self.e = Enemy(self, 500, ALTURA - 40, 200)
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
        global FPS
        #Atualiza o loop
        self.todas_sprites.update()
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top 
                self.player.vel.y = 0 
                
        if self.player.rect.right >= LARGURA/2:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x + 0.5*self.player.acc.x)
            
            for enemy in self.enemys:
                enemy.pos.x -= abs(self.player.vel.x + 0.5*self.player.acc.x)
        
        for enemy in self.enemys:        
            if enemy.vel.y > 0:
                hits = pygame.sprite.spritecollide(enemy, self.platforms, False)
                if hits:
                    enemy.pos.y = hits[0].rect.top
                    enemy.vel.y = 0
        
        if self.player.rect.right < LARGURA/2:         
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x + 0.5*self.player.acc.x)

            for enemy in self.enemys:
                enemy.pos.x += abs(self.player.vel.x + 0.5*self.player.acc.x)


        for enemy in self.enemys:
            if self.distancia(self.player, enemy) < 150 and not self.bool_contato:
                FPS = 20
                self.bool_contato = True
                self.end_time = pygame.time.get_ticks() + 3000
                for i in range(50,350,100):
                    seta = Setas(self, i)
                    self.grupo_setas.add(seta)
                    self.todas_sprites.add(seta)

        self.current_time = pygame.time.get_ticks()
        if self.end_time < self.current_time:
            FPS = 60
            self.bool_contato = False
            for seta in self.grupo_setas:
                self.grupo_setas.remove()
                self.todas_sprites.remove(seta)
                
    def events(self):
        #Eventos do loop
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.player.jump()
                
                if (evento.key == pygame.K_ESCAPE):
                    if self.playing:
                        self.playing = False
                        self.running = False
                    
                            
    def draw(self):
        #Desenha as imagens
        self.tela.fill(GREEN2)
   
        self.todas_sprites.draw(self.tela)
        
        #Sempre que desenhar use isso
        pygame.display.flip()
    
    def show_start_screen(self):
        
        self.tela.fill(BLUE)
        self.draw_text(TITLE, 48, WHITE, LARGURA/2, ALTURA/4)
        self.draw_text("Press Start", 30, WHITE, LARGURA/2, ALTURA/2)
        self.draw_text("Quit [Esc]", 30, WHITE, LARGURA/2, 400)
        pygame.display.flip()
        self.wait_for_key()
        
    def show_go_screen(self):
        
        pass
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:

                    waiting = False
                    self.running = False
                
                if (evento.type == pygame.KEYDOWN) and (evento.key == pygame.K_RETURN):
                    waiting = False
                    self.running = True
                
                if (evento.type == pygame.KEYDOWN) and (evento.key == pygame.K_ESCAPE):
                    waiting = False
                    self.running = False
                
           
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.tela.blit(text_surface, text_rect)

    def distancia(self, obj1, obj2):
        self.dif_x = math.fabs(obj1.pos.x) - math.fabs(obj2.pos.x)
        self.dif_y = math.fabs(obj1.pos.y) - math.fabs(obj2.pos.y)
        self.pit = math.sqrt(self.dif_x**2 + self.dif_y**2)
        return self.pit


g = Game()
g.show_start_screen()

while g.running:

    g.new()
    g.show_go_screen()
    
pygame.quit() 
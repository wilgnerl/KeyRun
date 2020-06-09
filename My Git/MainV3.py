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
        self.confronto_liberado = True
        self.acertos = 0
        self.start = pygame.time.get_ticks()
        self.cod_enemy = 0
        self.vidas = VIDAS
        self.setas_apertadas = 0
    
    def load_data(self):
        self.dir = os.path.dirname(__file__)
        img_dir = os.path.join(self.dir, 'Tiles')
        self.spritesheet_enemy = Spritesheet(os.path.join(img_dir, SPRITESHEET_ENEMY))
        self.spritesheet_keys = Spritesheet(os.path.join(img_dir, SPRITESHEE_KEYS))
        self.image_heart = pygame.image.load(os.path.join(img_dir, HEART_PNG)).convert_alpha()

    def new(self):
        #Inicia o jogo
        self.todas_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.grupo_setas = pygame.sprite.Group()
        self.grupo_setas_certo = pygame.sprite.Group()
        self.grupo_setas_errado = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.grupo_coracoes = pygame.sprite.Group()

        assets = load_assets(imagem1)
        
        for row in range(len(MAP)):
            for column in range(len(MAP[row])):
                tile_type = MAP[row][column]
                if tile_type == 3:
                    tile = Tile(assets[tile_type], row, column)
                    self.background.add(tile)
                    self.todas_sprites.add(tile) 
                    
                else:
                    tile = Tile(assets[tile_type], row, column)
                    self.platforms.add(tile)
                    self.todas_sprites.add(tile)

        for vida in range(VIDAS):
            x_pos = [1180, 1250, 1320]
            self.coracao = Coracao(self, x_pos[vida], vida)
            self.todas_sprites.add(self.coracao)
            self.grupo_coracoes.add(self.coracao)
            

        self.player = Player(self)
        self.todas_sprites.add(self.player) 

    
        self.e = Enemy(self, 700, ALTURA - 40, 200)
        self.todas_sprites.add(self.e)
        self.enemys.add(self.e)
        self.cod_enemy += 1
        
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

        if DIFICULDADE == 'facil':
            self.dificuldade_setas = 300
        elif DIFICULDADE == 'medio':
            self.dificuldade_setas = 500
        elif DIFICULDADE == 'dificil':
            self.dificuldade_setas = 700
        elif DIFICULDADE == 'god':
            self.dificuldade_setas = 900

        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top 
                self.player.vel.y = 0 
        
        for enemy in self.enemys:        
            if enemy.vel.y > 0:
                hits = pygame.sprite.spritecollide(enemy, self.platforms, False)
                if hits:
                    enemy.pos.y = hits[0].rect.top
                    enemy.vel.y = 0

        # Spawna inimigos a cada 10 segundos
        self.now = pygame.time.get_ticks()
        if self.now - self.start > TEMPO_SPAWN_INIMIGO:
            self.enemy = Enemy(self, random.randint(40,1200), random.randint(1,ALTURA - 60), random.randint(100,200))
            self.todas_sprites.add(self.enemy)
            self.enemys.add(self.enemy)
            self.start = self.now
            self.cod_enemy += 1
        
        # Verifica a distancia entre inimigo e player para assim ativar modo slowmotion
        for enemy in self.enemys:
            if self.distancia(self.player, enemy) < 150 and self.confronto_liberado:
                FPS = 20
                self.confronto_liberado = False
                self.end_time = pygame.time.get_ticks() + 3000
                self.lista_setas_tela = []
                self.setas_apertadas = 0
                self.pos_seta = 0
                self.cod_seta = 0
                self.acertos = 0
                self.enemy_fight = enemy
                for i in range(50, self.dificuldade_setas, 100):
                    seta = Setas(self, i, self.cod_seta)
                    self.lista_setas_tela.append(seta.retorno())
                    self.grupo_setas.add(seta)
                    self.todas_sprites.add(seta)
                    self.cod_seta += 1

        if not self.confronto_liberado:
            self.current_time = pygame.time.get_ticks()

            if self.end_time < self.current_time or self.setas_apertadas == self.cod_seta and not self.confronto_liberado:
                FPS = 60
                if self.acertos == self.setas_apertadas and self.setas_apertadas != 0:
                    self.enemy_fight.kill()
                else:
                    self.vidas -= 1
                    for coracao in self.grupo_coracoes:
                        if coracao.cod == self.vidas:
                            self.grupo_coracoes.remove(coracao)
                            self.todas_sprites.remove(coracao)
            
                for seta in self.grupo_setas:
                    self.grupo_setas.remove(seta)
                    self.todas_sprites.remove(seta)
                for seta in self.grupo_setas_certo:
                    self.grupo_setas_certo.remove(seta)
                    self.todas_sprites.remove(seta)
                for seta in self.grupo_setas_errado:
                    self.grupo_setas_errado.remove(seta)
                    self.todas_sprites.remove(seta)

                self.confronto_liberado = True

        if self.vidas == 0:
            self.running = False
            self.playing = False
                
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

                if evento.key == pygame.K_UP:
                    for seta in self.grupo_setas:
                        if seta.cod == self.pos_seta:
                            if seta.sentido == 'cima':
                                seta.acerto()
                                break
                            else:
                                seta.erro()
                                break

                if evento.key == pygame.K_DOWN:
                    for seta in self.grupo_setas:
                        if seta.cod == self.pos_seta:
                            if seta.sentido == 'baixo':
                                seta.acerto()
                                break
                            else:
                                seta.erro()
                                break

                if evento.key == pygame.K_RIGHT:
                    for seta in self.grupo_setas:
                        if seta.cod == self.pos_seta:
                            if seta.sentido == 'direita':
                                seta.acerto()
                                break
                            else:
                                seta.erro()
                                break

                if evento.key == pygame.K_LEFT:
                    for seta in self.grupo_setas:
                        if seta.cod == self.pos_seta:
                            if seta.sentido == 'esquerda':
                                seta.acerto()
                                break
                            else:
                                seta.erro()
                                break

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
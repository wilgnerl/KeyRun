import pygame, random, math
from Configs import *
from Sprites import *

# Classe principal do jogo

class Game:

    def __init__(self):

        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))   # Inicia Tela
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()   # Carrega arquivos
        self.end_time = 0
        self.confronto_liberado = True  # Libera confronto entre inimigo e player
        self.acertos = 0   # Setas acertadas
        self.start = pygame.time.get_ticks()
        self.cod_enemy = 0  # Variável de código para identificar cada inimigo e seta
        self.vidas = 3  # Vidas do jogador
        self.setas_apertadas = 0  # Controle de quantas setas foram apertdas
        self.dificuldade = 'facil'  # Dificuldade do jogo
        self.placar = 0  # Pontuação do player
        self.tempo_spawn_inimigo = 10000   # Defini o tempo de spawn do inimigo
        self.dificuldade_setas = 300  # Quantidade de setas (dividir valor por 100)
        font1 = pygame.font.Font(pygame.font.get_default_font(), 60)
        font2 = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.score = font2.render(' SCORE', True, BLACK)  # Print inicial da pontuação
        self.pontos = font1.render(' 0', True, BLACK)
        self.movement = True

    # Função que carrega as músicas
    def musica(self): 
        musica = os.path.join("sons", "Common Fight.ogg")
        pygame.mixer.music.load(musica)
        pygame.mixer.music.play(-1)

    # Função que carrega arquivos e suas localizações
    def load_data(self):
        self.dir = os.path.dirname(__file__)
        img_dir = os.path.join(self.dir, 'Tiles')
        self.spritesheet_enemy = Spritesheet(os.path.join(img_dir, SPRITESHEET_ENEMY), 3)
        self.spritesheet_keys = Spritesheet(os.path.join(img_dir, SPRITESHEE_KEYS), 3)
        self.image_heart = pygame.image.load(os.path.join(img_dir, HEART_PNG)).convert_alpha()
        self.spritesheet_hero = Spritesheet(os.path.join(img_dir, SPRITESHEET_HERO), 5)

    # Função que cria os grupos para os collides e que inicia os componentes visuais, como inimigo, player, tiles e corações de vida
    def new(self):
        #Inicia o jogo

        #Grupos para collide
        self.todas_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.grupo_setas = pygame.sprite.Group()
        self.grupo_setas_certo = pygame.sprite.Group()
        self.grupo_setas_errado = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.grupo_coracoes = pygame.sprite.Group()

        assets = load_assets(imagem1)
        
        # Loop para geração do cenário
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

        # Loop para gerar os corações
        for vida in range(self.vidas):
            x_pos = [1180, 1250, 1320]
            self.coracao = Coracao(self, x_pos[vida], vida)
            self.todas_sprites.add(self.coracao)
            self.grupo_coracoes.add(self.coracao)

        #Inicia o player
        self.player = Player(self)
        self.todas_sprites.add(self.player) 

        # Primeiro inimigo a ser gerado
        self.e = Enemy(self, 900, ALTURA - 40, 200)
        self.todas_sprites.add(self.e)
        self.enemys.add(self.e)
        self.cod_enemy += 1
        
        self.run()
     
    # Função que inicia outros métodos
    def run(self):
        #Inicia Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    # Função de atualização do jogo
    def update(self):

        global FPS

        #Atualiza as sprites
        self.todas_sprites.update()

        # Define a dificuldade do jogo de acordo com a pontuação do jogador
        if self.placar == 5:
            self.dificuldade = 'medio'
            self.dificuldade_setas = 500
            self.tempo_spawn_inimigo = 9000
        elif self.placar == 10:
            self.dificuldade = 'dificil'
            self.dificuldade_setas = 700
            self.tempo_spawn_inimigo = 8000
        elif self.placar == 15:
            self.dificuldade = 'gof'
            self.dificuldade_setas = 900
            self.tempo_spawn_inimigo = 7000

        # Controle entre plataformas e player/inimigo
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
        if self.now - self.start > self.tempo_spawn_inimigo:
            self.enemy = Enemy(self, random.randint(40,1200), random.randint(100,ALTURA - 60), random.randint(100,200))
            self.todas_sprites.add(self.enemy)
            self.enemys.add(self.enemy)
            self.start = self.now
            self.cod_enemy += 1
        
        # Verifica a distancia entre inimigo e player para assim ativar setas e slowmotion
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
                self.movement = False

                # Gera as setas
                for i in range(30, self.dificuldade_setas, 100):
                    seta = Setas(self, i, self.cod_seta)
                    self.lista_setas_tela.append(seta.retorno())
                    self.grupo_setas.add(seta)
                    self.todas_sprites.add(seta)
                    self.cod_seta += 1

        # Após acabar o confronto, verifica se tira vida do player ou mata o inimigo. Também retorna o FPS para 60
        if not self.confronto_liberado:
            self.current_time = pygame.time.get_ticks()
            if self.end_time < self.current_time or self.setas_apertadas == self.cod_seta and not self.confronto_liberado:

                #Player ganha o confronto
                if self.acertos == self.setas_apertadas and self.setas_apertadas != 0:
                    FPS = 60
                    self.enemys.remove(self.enemy_fight)
                    self.enemy_fight.kill()
                    self.confronto_liberado = True
                    self.movement = True

                #Player perde o confronto
                else:
                    self.vidas -= 1
                    FPS = 60
                    self.player.damage(self.enemy_fight)
                    self.movement = True
                    for coracao in self.grupo_coracoes:
                        if coracao.cod == self.vidas:
                            self.grupo_coracoes.remove(coracao)
                            self.todas_sprites.remove(coracao)
                            self.confronto_liberado = True

                # Deleta as setas dos grupos
                for seta in self.grupo_setas:
                    self.grupo_setas.remove(seta)
                    self.todas_sprites.remove(seta)
                for seta in self.grupo_setas_certo:
                    self.grupo_setas_certo.remove(seta)
                    self.todas_sprites.remove(seta)
                for seta in self.grupo_setas_errado:
                    self.grupo_setas_errado.remove(seta)
                    self.todas_sprites.remove(seta)

        # Se acabarem as vidas do player ele morre aqui
        if self.vidas == 0:
            self.running = False
            self.playing = False
                
        # Print do score
        font1 = pygame.font.Font(pygame.font.get_default_font(), 60)
        font2 = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.score = font2.render(' SCORE', True, BLACK)
        self.pontos = font1.render(' {}'.format(self.placar*200), True, BLACK)
        
    def events(self):

        #Eventos do loop
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False

            # Pulo do player
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.player.jump()
                    self.player.jumping
                
                if (evento.key == pygame.K_ESCAPE):
                    if self.playing:
                        self.playing = False
                        self.running = False

                # Verifica o evento de resposta das setas quando entra em confronto com o inimigo
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

    # Desenha as imagens
    def draw(self):
        self.tela.fill(GREEN2)
        self.todas_sprites.draw(self.tela)
        self.tela.blit(self.pontos, (0, ALTURA - 60))
        self.tela.blit(self.score, (12, ALTURA - 90))
        
        pygame.display.flip()
    
    # Tela de inicio
    def show_start_screen(self):
        
        self.tela.fill(BLUE)
        self.draw_text(TITLE, 48, WHITE, LARGURA/2, ALTURA/4)
        self.draw_text("Press Start", 30, WHITE, LARGURA/2, ALTURA/2)
        self.draw_text("Quit [Esc]", 30, WHITE, LARGURA/2, 400)
        pygame.display.flip()
        self.wait_for_key()
        
    # Tela de GameOver
    def show_go_screen(self):
        
        self.tela.fill(BLACK)
        self.draw_text('Game Over', 60, WHITE , LARGURA/2, 300)
        self.draw_text('Aperte [Esc] Para Sair', 30, WHITE, LARGURA/2, 400)
        self.draw_text('Aperte [X] Para começar novamente', 30 , WHITE, LARGURA/2, 450)
        self.draw_text('Sua pontuação: {}'.format(self.placar*200), 30, WHITE, LARGURA/4, 600)
        pygame.display.flip()
        self.wait_for_key()
       
        
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
                    self.musica()                  
                    
                if (evento.type == pygame.KEYDOWN) and (evento.key == pygame.K_ESCAPE):
                    waiting = False
                    self.running = False
                    
                if (evento.type == pygame.KEYDOWN) and (evento.key == pygame.K_x):
                    print('Apertei X')
                    waiting = False
                    self.running = True
                    self.musica()
                    self.vidas = 3
                    self.placar = 0
                    self.dificuldade = 'facil' 

    # Função usada para desenhar na tela de acordo com alguns inputs
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.tela.blit(text_surface, text_rect)

    # Função que calcula a distância entre o player o inimigo mais proximo para assim iniciar o modo de confronto
    def distancia(self, obj1, obj2):
        self.dif_x = math.fabs(obj1.pos.x) - math.fabs(obj2.pos.x)
        self.dif_y = math.fabs(obj1.pos.y) - math.fabs(obj2.pos.y)
        self.pit = math.sqrt(self.dif_x**2 + self.dif_y**2)
        return self.pit

    def dist_x(self, obj1, obj2):
        self.dif_x = obj1.pos.x - obj2.pos.x
        if self.dif_x > 0:
            return True
        else:
            return False

g = Game()
g.show_start_screen()

# Loop principal
while g.running:

    g.new()
    g.show_go_screen()   
    
pygame.quit() 
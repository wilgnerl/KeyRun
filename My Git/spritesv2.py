import pygame
import os
import random
import time
from Configurações import *
vec = pygame.math.Vector2

#Configurando pasta e Assets(Figura que vai ser o player)
pasta = os.path.dirname(__file__)
imagem1 = os.path.join(pasta, "Tiles")

   
def load_spritesheet(spritesheet, rows, columns):
    # Calcula a largura e altura de cada sprite.
    sprite_width = spritesheet.get_width() // columns
    sprite_height = spritesheet.get_height() // rows
    
    # Percorre todos os sprites adicionando em uma lista.
    sprites = []
    for row in range(rows):
        for column in range(columns):
            # Calcula posição do sprite atual
            x = column * sprite_width
            y = row * sprite_height
            # Define o retângulo que contém o sprite atual
            dest_rect = pygame.Rect(x, y, sprite_width, sprite_height)

            # Cria uma imagem vazia do tamanho do sprite
            image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            # Copia o sprite atual (do spritesheet) na imagem
            image.blit(spritesheet, (0, 0), dest_rect)
            sprites.append(image)
    return sprites

class Player(pygame.sprite.Sprite):
    
    def __init__(self, game):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        player = os.path.join(pasta, "Tiles") 
        self.player_sheet = pygame.image.load(os.path.join(player, "Hero1.gif")).convert_alpha()
        #self.player_sheet.set_colorkey(WHITE)
        # Aumenta o tamanho do spritesheet para ficar mais fácil de ver
        self.player_sheet = pygame.transform.scale(self.player_sheet, (300, 300))
        
        
        # Define sequências de sprites de cada animação
        spritesheet = load_spritesheet(self.player_sheet, 4, 4)
        self.animations = {
            STILL: spritesheet[0:4],
            WALKING: spritesheet[4:7],
            JUMPING: spritesheet[0:4],
            FIGHTING: spritesheet[8:12],
            SWIMMING: spritesheet[12:16],
        }
        
        # Define estado atual (que define qual animação deve ser mostrada)
        self.state = STILL
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza na tela.
        self.rect.center = (ALTURA/2, LARGURA/2)
        
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 300
        
        self.pos = vec(ALTURA/2, LARGURA/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20 
               
    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Atualiza animação atual
            self.animation = self.animations[self.state]
            # Reinicia a animação caso o índice da imagem atual seja inválido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posição do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            
        self.acc = vec(0,GRAVIDADE)
        self.vy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
            self.state = WALKING
            
        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC
            self.state = WALKING
        
        else:
            self.state = STILL
            
            
        self.acc.x += self.vel.x * PLAYER_FRICTION            
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.rect.midbottom = self.pos
        
        if self.pos.x >= 700:
            self.pos.x = 2
            
        if self.pos.x < 0:
            self.pos.x = 695
              
class Spritesheet():
    
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, heigth):
        image = pygame.Surface((width, heigth))
        image.blit(self.spritesheet, (0,0), (x, y, width, heigth))
        image = pygame.transform.scale(image, (width * 3, heigth * 3))
        return image       
        
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, game, x, y, distance):
        pygame.sprite.Sprite.__init__(self)
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
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.end = x + distance
        self.start = x
        
    def update(self):

        self.animate()
        self.acc = vec(0,GRAVIDADE)
        self.vel.y = 3
        if self.vel.x >= 0 and self.rect.x < self.end:
            self.vel.x = 0.8
        elif self.rect.x == self.end:
            self.vel.x = -0.8
        elif self.vel.x < 0 and self.rect.x > self.start:
            self.vel.x = -0.8
        elif self.rect.x == self.start:
            self.vel.x = 0.8

        self.acc.x += self.vel.x * PLAYER_FRICTION            
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.rect.midbottom =  self.pos
        
        '''if self.pos.x >= 1000:
            self.pos.x = 1000
        if self.pos.x < 0:
            self.pos.x = 0'''

    def animate(self):
        
        now = pygame.time.get_ticks()

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
                
    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.groupcollide(self, self.game.platforms, False, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20 
                
    def load_images(self):
        self.standing_frames = [self.game.spritesheet_enemy.get_image(112, 19, 16, 13), #0
                            self.game.spritesheet_enemy.get_image(112, 19, 16, 13),
                            self.game.spritesheet_enemy.get_image(112, 19, 16, 13),
                            self.game.spritesheet_enemy.get_image(128, 19, 16, 13)] #1
        
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
            
        self.walk_frames_l = [self.game.spritesheet_enemy.get_image(112, 35, 14, 13),  #2
                            self.game.spritesheet_enemy.get_image(129, 35, 14, 13),  #3
                            self.game.spritesheet_enemy.get_image(145, 35, 16, 13),  #4
                            self.game.spritesheet_enemy.get_image(160, 35, 16, 13),  #5
                            self.game.spritesheet_enemy.get_image(176, 35, 16, 13),  #6
                            self.game.spritesheet_enemy.get_image(192, 35, 16, 13)]  #7
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)
            
        self.walk_frames_r = []

        for frame in self.walk_frames_l:
            self.walk_frames_r.append(pygame.transform.flip(frame, True, False))

class Setas(pygame.sprite.Sprite):

    def __init__(self, game, x, cod):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.load_images()
        self.lista_opcoes =  ['cima', 'baixo', 'direita', 'esquerda']
        self.sentido = random.choice(self.lista_opcoes)
        if self.sentido == 'cima':
            self.image = self.seta_cima
        elif self.sentido == 'baixo':
            self.image = self.seta_baixo
        elif self.sentido == 'direita':
            self.image = self.seta_direita
        else:
            self.image = self.seta_esquerda

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = 50
        self.rect.x = x
        self.pos = (self.rect.x, self.rect.y)
        self.cod = cod


    def retorno(self):
        return self.sentido

    def load_images(self):
        
        self.seta_cima = self.game.spritesheet_keys.get_image(32,0,32,32)
        self.seta_baixo = self.game.spritesheet_keys.get_image(32,32,32,32)
        self.seta_esquerda = self.game.spritesheet_keys.get_image(0,32,32,32)
        self.seta_direita = self.game.spritesheet_keys.get_image(64,32,32,32)

        self.seta_cima_erro = self.game.spritesheet_keys.get_image(0,64,32,32)
        self.seta_baixo_erro = self.game.spritesheet_keys.get_image(64,64,32,32)
        self.seta_esquerda_erro = self.game.spritesheet_keys.get_image(0,0,32,32)
        self.seta_direita_erro = self.game.spritesheet_keys.get_image(64,0,32,32)

        self.seta_cima_acerto = self.game.spritesheet_keys.get_image(32,128,32,32)
        self.seta_baixo_acerto = self.game.spritesheet_keys.get_image(32,160,32,32)
        self.seta_esquerda_acerto = self.game.spritesheet_keys.get_image(0,160,32,32)
        self.seta_direita_acerto = self.game.spritesheet_keys.get_image(64,160,32,32)

    def img_acerto(self):

        if self.sentido == 'cima':
            self.image = self.seta_cima_acerto
        elif self.sentido == 'baixo':
            self.image = self.seta_baixo_acerto
        elif self.sentido == 'direita':
            self.image = self.seta_direita_acerto
        else:
            self.image = self.seta_esquerda_acerto

    def img_erro(self):

        if self.sentido == 'cima':
            self.image = self.seta_cima_erro
        elif self.sentido == 'baixo':
            self.image = self.seta_baixo_erro
        elif self.sentido == 'direita':
            self.image = self.seta_direita_erro
        else:
            self.image = self.seta_esquerda_erro

    def acerto(self):
        self.game.grupo_setas.remove(self)
        self.game.todas_sprites.remove(self)
        self.img_acerto()
        self.game.grupo_setas_certo.add(self)
        self.game.todas_sprites.add(self)
        self.game.pos_seta += 1

    def erro(self):
        self.game.grupo_setas.remove(self)
        self.game.todas_sprites.remove(self)
        self.img_erro()
        self.game.todas_sprites.add(self)
        self.game.grupo_setas_errado.add(self)
        self.game.pos_seta += 1

class Coracao(pygame.sprite.Sprite):

    def __init__(self, game, x, cod):
        pass
    
class Tile(pygame.sprite.Sprite):
    
    def __init__(self, tile_img, row, column):
    
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))

        # Define a imagem do tile.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Posiciona o tile
        self.rect.x = TILE_SIZE * column
        self.rect.y = TILE_SIZE * row
        
def load_assets(img):
    assets = {}
    assets[CHAO] = pygame.image.load(os.path.join(imagem1, "grassMid.png")).convert()
    assets[TERRA] = pygame.image.load(os.path.join(imagem1, "grassCenter.png")).convert()
    assets[CEU] = pygame.image.load(os.path.join(imagem1, "liquidWater.png")).convert()
    return assets
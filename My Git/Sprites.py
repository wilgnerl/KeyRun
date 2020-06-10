import pygame, os, random
from Configs import *

vec = pygame.math.Vector2

#Configurando pasta e Assets(Figura que vai ser o player)
pasta = os.path.dirname(__file__)
imagem1 = os.path.join(pasta, "Tiles")

class Player(pygame.sprite.Sprite):
    
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA / 2, ALTURA / 2)
        self.pos = vec(LARGURA / 2, ALTURA / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet_hero.get_image(19, 114, 10, 14),
                                self.game.spritesheet_hero.get_image(35, 114, 10, 14),
                                self.game.spritesheet_hero.get_image(51, 114, 10, 14),
                                self.game.spritesheet_hero.get_image(67, 114, 10, 14)]
        
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        
        self.walk_frames_r = [self.game.spritesheet_hero.get_image(19, 146, 11, 14),
                              self.game.spritesheet_hero.get_image(35, 146, 11, 14),
                              self.game.spritesheet_hero.get_image(51, 146, 11, 14)]
        
        self.walk_frames_l = []
        
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))
        
        
        '''self.jump_frames_r = [self.game.spritesheet_hero.get_image(17, 193, 14, 14),
                           self.game.spritesheet_hero.get_image(33, 193, 14, 14)]        

        
        for frame in self.jump_frames_r:
            frame.set_colorkey(BLACK)
            self.jump_frames_l.append(pygame.transform.flip(frame, True, False))'''
        
        

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0, GRAVIDADE)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > LARGURA + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = LARGURA + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        
        '''if self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.jump_frames_r[self.current_frame]
                else:
                    self.image = self.jump_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom'''
                
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom    
              
class Spritesheet():
    
    def __init__(self, filename, mult):
        self.spritesheet = pygame.image.load(filename).convert_alpha()
        self.mult = mult

    def get_image(self, x, y, width, heigth):
        image = pygame.Surface((width, heigth))
        image.blit(self.spritesheet, (0,0), (x, y, width, heigth))
        image = pygame.transform.scale(image, (width * self.mult, heigth * self.mult))
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
        self.animar = True
        self.sumir = False
        
        
    def update(self):
        
        if self.animar:
            self.animate()
        self.acc = vec(0, GRAVIDADE)
        self.vy = 0
        if not self.sumir:
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
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.pos.y += self.vel.y + 1 * self.acc.y
        
        self.rect.midbottom = self.pos

        if self.pos.x >= 1400:
            self.pos.x = 2
            
        if self.pos.x < 0:
            self.pos.x = 1398

        self.current_time = pygame.time.get_ticks()

        if self.sumir:
            if self.end_time + 1500 < self.current_time and self.sumir:
                self.game.todas_sprites.remove(self)
                self.game.confronto_liberado = True
        

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

    
    def kill(self):
        
        self.vel.y = -10
        self.animar = False
        self.image = self.standing_frames[0]
        self.end_time = pygame.time.get_ticks() + 500
        self.sumir = True
        self.game.placar += 1

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
        self.rect.y = 30
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
        self.game.setas_apertadas += 1
        self.game.acertos += 1

    def erro(self):
        self.game.grupo_setas.remove(self)
        self.game.todas_sprites.remove(self)
        self.img_erro()
        self.game.todas_sprites.add(self)
        self.game.grupo_setas_errado.add(self)
        self.game.pos_seta += 1
        self.game.setas_apertadas += 1

class Coracao(pygame.sprite.Sprite):

    def __init__(self, game, x, cod):

        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(self.game.image_heart, (64,64))
        self.cod = cod
        self.rect = self.game.image_heart.get_rect()
        self.rect.y = 30
        self.rect.x = x
        self.pos = (self.rect.x, self.rect.y)
  
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
        self.image.set_colorkey(BLACK)

        # Posiciona o tile
        self.rect.x = TILE_SIZE * column
        self.rect.y = TILE_SIZE * row
        
def load_assets(img):
    assets = {}
    assets[CHAO] = pygame.image.load(os.path.join(imagem1, "grassMid.png")).convert()
    assets[TERRA] = pygame.image.load(os.path.join(imagem1, "grassCenter.png")).convert()
    assets[CEU] = pygame.image.load(os.path.join(imagem1, "liquidWater.png")).convert()
    assets[BASE] = pygame.image.load(os.path.join(imagem1, "sandMid.png")).convert()
    assets[BASE_E] = pygame.image.load(os.path.join(imagem1, "sandLeft.png")).convert_alpha()
    assets[BASE_D] = pygame.image.load(os.path.join(imagem1, "sandRight.png")).convert_alpha()
    
    return assets
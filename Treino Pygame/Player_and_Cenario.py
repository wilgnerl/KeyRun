import pygame
import sys
import os

TITULO = 'Teste 1'
LARGURA = 480
ALTURA = 600
TILE_SIZE = 40
FPS = 60

#Cores para ser utilizada
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Definindo cenario
CHAO = 1
CHAO2 = 2
CEU = 3

#15 linhas x 12 Colunas
#Dividi altura e largura da tela pelo tamanho do quadradinho
MAP = [
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU, CEU],
    [CHAO2, CHAO2, CHAO2, CHAO2, CHAO2, CHAO2, CHAO2, CHAO2, CHAO2, CHAO2, CHAO2, CHAO2],
    [CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO],               #12
    [CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO],
    [CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO],
    [CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO, CHAO],
]

#Configurando pasta e Assets(Figura que vai ser o player)
pasta = os.path.dirname(__file__)
imagem1 = os.path.join(pasta, "pactiles")
img_dir = os.path.join(pasta, "Tiles")

#Criando Jogador
class Jogador(pygame.sprite.Sprite):

    #Caracteristicas do jogador
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Fala quem é a imagem
        self.image = pygame.image.load(os.path.join(imagem1, "pac.png")).convert()
        self.image.set_colorkey(WHITE)
        #Determina posição inicial da imagem
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA/2, ALTURA-400)
        
        self.speedx = 0
        self.speedy = 0
    
    #Atualiza informações sobre o jogador   
    def update(self):
        self.speedx = 0
        self.speedy = 0
        #Verifica botão apertad
        botão = pygame.key.get_pressed()
        if botão[pygame.K_LEFT]:
            self.speedx = -5
        
        if botão[pygame.K_RIGHT]:
            self.speedx = 5
        
        if botão[pygame.K_UP]:
            self.speedy = -5
            
        if botão[pygame.K_DOWN]:
            self.speedy = 5
            
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA
        
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.rect.bottom > 400:
            self.rect.bottom = 400
        

        self.rect.x += self.speedx
        self.rect.y += self.speedy

#Criando classe para cenario    
class Tile(pygame.sprite.Sprite):
    
    def __init__(self, tile_img, linha, coluna):
        
        pygame.sprite.Sprite.__init__(self)
        
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
        self.image = tile_img
        self.rect = self.image.get_rect()
        self.rect.x = TILE_SIZE * coluna
        self.rect.y = TILE_SIZE * linha

#Função que carrega o cenario 
def load_tile(img_dir):
    assets = {}
    assets[CHAO] = pygame.image.load(os.path.join(img_dir, 'grassCenter.png')).convert()
    assets[CHAO2] = pygame.image.load(os.path.join(img_dir, 'grassMid.png')).convert()
    assets[CEU] = pygame.image.load(os.path.join(img_dir, 'liquidWater.png')).convert()
    return assets

#Função que roda o cenario
def tela(TELA):
    assets = load_tile(img_dir)
    tiles = pygame.sprite.Group()
    
    for linha in range(len(MAP)):
        for coluna in range(len(MAP[linha])):
            tile_type = MAP[linha][coluna]
            tile  = Tile(assets[tile_type], linha, coluna)
            tiles.add(tile)

    clock = pygame.time.Clock()

    todas_sprites = pygame.sprite.Group()
    p1 = Jogador()
    todas_sprites.add(p1)

    game = True
    while game:
        #Velocidade do looping
        clock.tick(FPS)
        #Eventos
        eventos = pygame.event.get()
        
        for eventos in eventos:
            if eventos.type == pygame.QUIT:
                game = False

                
        #Atualizações
        todas_sprites.update()
        #Desenhos e renderizações
        TELA.fill(BLACK)
        tiles.draw(TELA)
        todas_sprites.draw(TELA)
        
        #Sempre que desenhar use isso
        pygame.display.flip()

#Inicia o pygame
pygame.init()

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

try:
    tela(TELA)

finally:
    pygame.quit()
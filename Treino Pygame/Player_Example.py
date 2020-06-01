import pygame
import sys
import os

TITULO = 'Teste 1'
LARGURA = 800
ALTURA = 800
TILE_SIZE = 40
FPS = 60

#Cores par aser utilizada
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


#Configurando pasta e Assets(Figura que vai ser o player)
pasta = os.path.dirname(__file__)
imagem1 = os.path.join(pasta, "pactiles")

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
        self.rect.center = (LARGURA/2, ALTURA/2)
        
        self.y_speed = 5
    
    #Atualiza informações sobre o jogador   
    def update(self):
        #Anda 5 unidades no eixo X para a direita
        self.rect.x += 5
        self.rect.y += self.y_speed
        
        if self.rect.bottom > ALTURA - 300:
            self.y_speed = - 5
            
        if self.rect.top < 300:
            self.y_speed = 5
            
        if self.rect.left > LARGURA:
            self.rect.right = 0
        
        
        
#Iniciando Pygame
pygame.init()

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
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
   
    todas_sprites.draw(TELA)
    
    #Sempre que desenhar use isso
    pygame.display.flip()
    
pygame.quit()
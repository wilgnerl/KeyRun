import pygame
import time
import sys

TITULO = 'Teste 1'
LARGURA = 480
ALTURA = 600
TILE_SIZE = 40
FPS = 60

#Cores par aser utilizada
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Iniciando Pygame
pygame.init()

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
clock = pygame.time.Clock()


todas_sprites = pygame.sprite.Group()

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
    TELA.fill(RED)
   
    todas_sprites.draw(TELA)
    
    #Sempre que desenhar use isso
    pygame.display.flip()
    
pygame.quit()
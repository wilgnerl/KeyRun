import pygame
import time
from Configurações import  *

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
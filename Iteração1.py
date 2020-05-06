import pygame
import random
import time

#Iniciando o jogo
pygame.init()

#Configurando a tela:
Largura = 600
Altura  = 600

tela = pygame.display.set_mode((Largura, Altura))           #Definindo tamando da tela
pygame.display.set_caption('Game')                          #Definindo titulo da tela

#Configurando imagem
LarguraObjeto = 50
AlturaObjeto = 50

background = pygame.image.load('cenario.png').convert()
background = pygame.transform.scale(background, (600, 600))
objeto_imagem = pygame.image.load('meteorBrown_med1.png').convert_alpha()
objeto_imagem = pygame.transform.scale(objeto_imagem, (LarguraObjeto, AlturaObjeto))


class Meteoro(pygame.sprite.Sprite):        #Configurando classe para o meteoro
    
    def __init__(self, img):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect  = self.image.get_rect()

        
meteoro = Meteoro(objeto_imagem)

#Configurando movimentação do objeto
def met (x,y):
    tela.blit(objeto_imagem, (x,y))

#Implantando Background 
def back():
    tela.blit(background, (0,0))

#Iniciando game
Game = True
x = 200
y = 200
#Looping que mantem o jogo funcionando
while Game:
    
    #Verifica ações dentro do jogo
    for event in pygame.event.get():
       
#Se a ação for a de clicar no X para fechar:
        if event.type == pygame.QUIT:
            Game = False
        
        #Calibrando movimentos
        #Verifica se alguma tecla foi apertada
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, muda posição
            if event.key == pygame.K_LEFT:
                x -= 8
            if event.key == pygame.K_RIGHT:
                x += 8
            if event.key == pygame.K_UP:
                y -= 8
            if event.key == pygame.K_DOWN:
                y += 8
                
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_LEFT:
                x -= 8
            if event.key == pygame.K_RIGHT:
                x += 8
            if event.key == pygame.K_UP:
                y -= 8
            if event.key == pygame.K_DOWN:
                y += 8
    
    #Gerando cor para a tela      
    tela.fill((0,255,0))
    back()
    met(x,y)
    
    #Atualizando a tela
    pygame.display.update()      
                    
    
  

    

#Configurando fechamento
pygame.quit()

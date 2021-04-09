import pygame, os, random
from Configs import *

class Musica:

    def __init__(self, som, canal):
        self.som = os.path.join("Snd", som)
        self.canal = canal

    def musica_de_fundo(self):
        '''
        Função que carrega a música de fundo (canal 0), que se repete sempre
        ''' 
        pygame.mixer.music.load(self.som)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    
    def efeitos_sonoros(self):
        '''
        Função que carrega as músicas de pulo e erro (canal 1)
        '''
        pygame.mixer.Channel(self.canal).play(pygame.mixer.Sound(self.som))
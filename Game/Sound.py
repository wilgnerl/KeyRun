import pygame
import os

# Classe sonora
class Sound:

    def __init__(self):
        self.musica = os.path.join("Snd", "Common Fight.ogg")
        self.volume = 0.1
        self.efeitos = {"Pulo": {"Canal": 1, "Arquivo": "Jump.ogg"},
                        "Matar": {"Canal": 1, "Arquivo": "Kill.ogg"},
                        "Lento": {"Canal": 2, "Arquivo": "lento.ogg"},
                        "Rapido": {"Canal": 2, "Arquivo": "rapido.ogg"},
                        "MorteInimigo": {"Canal": 3, "Arquivo": "Death_Enemy.ogg"},
                        "DanoPlayer": {"Canal": 3, "Arquivo": "PlayerDamage.ogg"}
                       }

    def playMusica(self):
        '''
        Função que carrega a música de fundo (canal 0), que se repete sempre
        ''' 
        try:
            pygame.mixer.music.load(self.musica)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
        except:
            None

    def efeitosSonoros(self, efeito):
        '''
        Função que carrega as músicas de pulo e erro (canal 1)
        '''
        try:
            self.pathEfeito = os.path.join("Snd", self.efeitos[efeito]["Arquivo"])
            pygame.mixer.Channel(self.efeitos[efeito]["Canal"]).play(pygame.mixer.Sound(self.pathEfeito))
        except:
            None
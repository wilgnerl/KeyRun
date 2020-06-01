# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame as py 
import random
from config import WIDTH, HEIGHT
from game_screen import game_screen


py.init()
py.mixer.init()

# ----- Gera tela principal
window = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Navinha')

game_screen(window)

# ===== Finalização =====
py.quit()  # Função do PyGame que finaliza os recursos utilizados


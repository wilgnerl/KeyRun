# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame

pygame.init()

# ----- Gera tela principal
window = pygame.display.set_mode((500, 400))
pygame.display.set_caption('Monica Game')

# ----- Inicia estruturas de dados
game = True

# ===== Loop principal =====
while game:
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Gera saídas
    window.fill((255, 255, 255))  # Preenche com a cor branca
    cor = (0, 255, 0) #Verde
    cor2 = (255,255, 0) #Amarelo
    cor3 = (0,0,255)  #Azul
    vertices = [(250, 0), (500, 200), (250, 400), (0, 200)]
    cubo = [(0,0), (500,0), (500,500), (0,500)]

    pygame.draw.polygon(window, cor, cubo)
    pygame.draw.polygon(window, cor2, vertices)
    pygame.draw.circle(window, cor3, [250, 200], 100, 100)
    

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados


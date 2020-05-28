#Configs iniciais de tela e FPS
TITLE = "Jumpy"
WIDTH = 1000
HEIGHT = 600
FPS = 60

#Player propertiers

PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12

# World props

GRAVITY = 1

#Starting platsforms

PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 300, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

# Enemy props

ENEMY_ACC = 0.3
ENEMY_FRICCTION = -0.12
ENEMY_GRAV = 1


#Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 ,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TESTE = (45, 76, 90)
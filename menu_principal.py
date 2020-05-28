
'''Arquivo para desenvolvimento do menu principal do PROJETO FINAL da matéria de Design de Software'''
#última edição por @fabricio_neri em 28 de maio às 20:45

#importando as bibliotecas para fazer o menu do JOGO
import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum

#definindo as cores necessárias para fazer o MENU
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Devolve uma surface com texto escrito """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    """ Uma interface do usuário que pode ser adicionada na surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Argumentos recebidos pela função:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - o jogo muda de acordo com essa ação
        """
        self.mouse_over = False
        #cria o botão
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )
        #cria o botão maiorzinho, quando o maouse passa por cima
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )
        #junta os dois em uma lista
        self.images = [default_image, highlighted_image]

        #cria o retangulo do botão
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0] #se o mouse estiver sobre o botão, vai fazer ela ficar maior

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ 
            Dá o UPDATE do mouse (variável) e 
            retorna a ação do botão quando clicado
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Desenha o elemnto na surface """
        surface.blit(self.image, self.rect)

#função principal do jogo, onde acontece o loop
def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE #STATE inicial do jogo

    while True:
        '''
            Aqui é o looping do jogo, e enquanto estiver em um STATE 'x', vai chamar a função que inicia alguma tela dependendo do STATE
        
        '''
        if game_state == GameState.TITLE:
            game_state = title_screen(screen) 

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


#define a função da tela do MENU e os seus botões
def title_screen(screen):
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

#aqui é uma função que exemplifica a mudança de tela de acordo com o botão apertado na tela menu.
#É mais um exemplo pra você que vai juntar os códigos, Will
def play_level(screen):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        pygame.display.flip()


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1


if __name__ == "__main__":
    main()
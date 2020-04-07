from pygame import display, Surface, colordict, draw
from pygame.color import THECOLORS

class Background:
    def __init__(self):
        # screen = display.get_surface()
        # back = Surface(screen.get_size()).convert()
        # back.fill((255, 255, 255))
        # self.image = back
        self.screen = display.get_surface()

    def update(self):
        pass  # Ainda não faz nada

    def draw(self):
        self.screen.fill(colordict.THECOLORS['white'])
        draw.rect(self.screen, THECOLORS['black'], [0, 0, 500, 500], 1)
        draw.rect(self.screen, THECOLORS['black'], [500, 0, 500, 150], 1)
        # draw.rect(self.screen, THECOLORS['black'], [500, 0, 150, 200], 1)

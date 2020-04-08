from pygame import display, draw
from pygame.color import THECOLORS


class Background:
    def __init__(self):

        self.screen = display.get_surface()

    def draw(self):
        self.screen.fill(THECOLORS['white'])
        draw.rect(self.screen, THECOLORS['black'], [0, 0, 500, 500], 1)
        draw.rect(self.screen, THECOLORS['black'], [500, 0, 500, 175], 1)


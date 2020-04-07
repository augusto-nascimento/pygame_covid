from pygame.sprite import Sprite
from pygame.color import THECOLORS
from pygame import Surface, draw
import pygame

from core import Report


class ChartReport(Sprite):

    def __init__(self, total_people: int):
        super(ChartReport, self).__init__()
        self.image = Surface([500, 500])
        self.image.fill(THECOLORS['white'])
        self.image.set_colorkey(THECOLORS['white'])
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 0
        self.__pause: int = 0
        self.total_people = total_people
        self.line_infected = [(0, 200)]
        self.report = Report()
        self.draw()

    def draw(self):
        pass

    def __draw_text(self):
        font = pygame.font.SysFont('Calibri', 14, True, False)
        count = 0
        for key, value in self.report.get_report().items():
            text = font.render(
                '{}: {}'.format(key, value.count),
                True,
                value.color
            )
            self.image.blit(text, [10, count])
            count += 20

        text = font.render(
            '{}: {}'.format('Máximo de Hospitalizados: ', self.report.max_sick),
            True,
            THECOLORS['black']
        )
        self.image.blit(text, [10, count])

    def __draw_line(self):
        if self.__pause:
            self.__pause -= 1
        else:
            scale = 1.5
            x = self.line_infected[-1][0] + 1
            total = (
                self.report.sick.count +
                self.report.sick_icu.count
            )
            y = int(round(500 - (total * scale), 0))
            self.line_infected.append((x, y))
            self.__pause = 1

        draw.lines(self.image, THECOLORS['black'], False, self.line_infected, 2)

    def __draw_total(self):
        if self.__pause:
            self.__pause -= 1
        else:
            scale = 1
            x = self.line_infected[-1][0] + 1
            total = (
                self.report.sick.count +
                self.report.sick_icu.count
            )
            y = int(round(500 - (total * scale), 0))
            self.line_infected.append((x, y))
            self.__pause = 1

        draw.lines(
            self.image,
            THECOLORS['black'],
            False,
            self.line_infected,
            2
        )

    def update(self):
        self.image.fill(THECOLORS['white'])
        self.__draw_text()
        self.__draw_line()

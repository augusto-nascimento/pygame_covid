from random import randint

from pygame.sprite import Sprite
from pygame.color import THECOLORS
from pygame import Surface, draw

from core import Report, StatusHealth
from config import parameters


class Person(Sprite):

    def __init__(
        self, position, status=StatusHealth.healthy
    ):
        super(Person, self).__init__()
        self.__status = None
        self.image: Surface = Surface([4, 4])
        self.__speed = 0  # 0 to 100
        self.__pause = 0
        self.__time_to_sick = parameters['time_to_sick'] * 50
        self.__time_after_sick = parameters['time_after_sick'] * 50
        self.report = Report()

        self.set_status(status)
        self.image.fill(THECOLORS['white'])
        self.image.set_colorkey(THECOLORS['white'])
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.direction_x = randint(5 * (-1), 5)
        self.direction_y = randint(5 * (-1), 5)

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.report.update(self.__status, status)
        self.__status = status

    def set_speed(self, speed=1):
        self.__speed = speed
        self.__pause = 100 - self.__speed
    
    def draw(self):
        draw.ellipse(
            self.image, self.__status.color, [0, 0, 4, 4], 0
        )        

    def update(self):

        if self.__status == StatusHealth.contaminated:
            if self.__time_to_sick:
                self.__time_to_sick -= 1
            else:
                p = randint(1, 100)
                if p <= 5:
                    self.set_status(StatusHealth.sick_icu)
                    self.set_speed(0)
                elif p <= 20:
                    self.set_status(StatusHealth.sick)
                    self.set_speed(10)
                else:
                    self.set_status(StatusHealth.recovered)
                    self.set_speed(100)

        if self.__status in [StatusHealth.sick, StatusHealth.sick_icu]:
            if self.__time_after_sick:
                self.__time_after_sick -= 1
            else:
                if self.__status == StatusHealth.sick:
                    self.set_status(StatusHealth.recovered)
                elif self.__status == StatusHealth.sick_icu:
                    if randint(1, 5) <= 2:
                        self.set_status(StatusHealth.dead)
                    else:
                        self.set_status(StatusHealth.recovered)
                        self.set_speed(100)

        if self.__pause:
            self.__pause -= 1
            return

        self.__pause = 100 - self.__speed
        screen_witdh, screen_height = 500, 500

        if (
            self.rect.x + self.direction_x > screen_witdh or
            self.rect.x + self.direction_x < 0
        ):
            self.direction_x = self.direction_x * (-1)
            self.direction_y = randint(5 * (-1), 5)

        self.rect.x += self.direction_x

        if (
            self.rect.y + self.direction_y > screen_height or
            self.rect.y + self.direction_y < 0
        ):
            self.direction_y = self.direction_y * (-1)
            self.direction_x = randint(5 * (-1), 5)

        self.rect.y += self.direction_y

        draw.ellipse(
            self.image, self.__status.color, [0, 0, 4, 4], 0
        )
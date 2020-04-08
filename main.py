# -*- coding: utf-8 -*-
import pygame
from random import randint

from pygame.locals import QUIT

from person import Person
from chart import ChartReport
from background import Background
from config import parameters
from core import Report, StatusHealth


class App:

    def __init__(self):
        
        self.size = [1000, 500]
        self.screen = pygame.display.set_mode(self.size, 0, 0)
        pygame.init()
        self.run = True
        self.infecteds = pygame.sprite.Group()
        self.healthy = pygame.sprite.Group()
        self.after_sick = pygame.sprite.Group()

    def handle_events(self):
        for event in pygame.event.get():
            t = event.type
            if t == QUIT:
                self.run = False

    def create_person(self) -> int:

        person_total = int(parameters['person_total'])
        person_contaminated = int(parameters['person_contaminated'])
        person_lockdown = int(parameters['person_lockdown'])

        # gerando pontos contaminados inicial
        for i in range(person_contaminated):
            x = randint(0, 500)
            y = randint(0, 500)

            person = Person((x, y), StatusHealth.contaminated)
            person.set_speed(100)
            self.infecteds.add(person)

        # Deixar grupo em lockdown no início da simulação
        for i in range(person_lockdown):
            x = randint(0, 500)
            y = randint(0, 500)

            person = Person((x, y))
            person.set_speed(0)
            self.healthy.add(person)

        # Criando restante dos pontos
        for i in range(person_total - person_contaminated - person_lockdown):
            x = randint(0, 500)
            y = randint(0, 500)
            person = Person((x, y))
            person.set_speed(100)
            self.healthy.add(person)

    def loop(self):

        # criando pessoas
        self.create_person()

        self.infecteds.draw(self.screen)
        self.healthy.draw(self.screen)

        clock = pygame.time.Clock()

        chart_report = pygame.sprite.RenderPlain(
            ChartReport()
        )

        while self.run:

            # criando o fundo
            self.background = Background()
            self.background.draw()

            # Manipulando eventos
            self.handle_events()

            # Atualiza Elementos
            self.healthy.update()
            self.infecteds.update()
            self.after_sick.update()

            collision = pygame.sprite.groupcollide(
                self.healthy, self.infecteds, False, False
            )

            # verifico se houve encontro entre pessoas
            # saudáveis e pessoas contaminadas
            for p in collision:
                if p.get_status() == StatusHealth.healthy:
                    p.set_status(StatusHealth.contaminated)
                    p.draw()
                    self.healthy.remove(p)
                    self.infecteds.add(p)

            # verifico se alguém que estava doente
            # se recuperou ou morreu
            for p in self.infecteds:
                if p.get_status() in [
                    StatusHealth.recovered, StatusHealth.dead
                ]:
                    self.infecteds.remove(p)
                    self.after_sick.add(p)

            # desenho as pessoas em suas novas posicoes e status
            self.infecteds.draw(self.screen)
            self.healthy.draw(self.screen)
            self.after_sick.draw(self.screen)

            # atualizo graficos
            chart_report.update()
            chart_report.draw(self.screen)
            pygame.display.flip()

            clock.tick(20)


if __name__ == '__main__':
    app = App()
    app.loop()

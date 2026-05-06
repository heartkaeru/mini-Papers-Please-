import pygame
from view import Screen


class GameController:
    def __init__(self):
        pygame.init()

        self.view = Screen()

    def run(self):
        while self.view.running:
            self.handle_events()
            self.view.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.view.running = False

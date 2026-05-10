import pygame
from view import Screen


class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.mixer.music.load('assets/sounds/bg.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

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

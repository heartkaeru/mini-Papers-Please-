import pygame

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption('Papers, please (radik edition)')
        self.myfont = pygame.font.Font(None, 40)

        icon = pygame.image.load('assets/images/icon.png')
        pygame.display.set_icon(icon)

        self.image = pygame.image.load('assets/images/minibro.png')
        self.image = pygame.transform.scale(self.image, self.screen.get_size())

        self.running = True
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill((224,176,255))

        image_rect = self.image.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(self.image, (0,0))

        pygame.display.update()
        self.clock.tick(60)

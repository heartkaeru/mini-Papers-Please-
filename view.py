import pygame

class Screen:
    def __init__(self):
        info = pygame.display.Info()
        WIDTH = info.current_w - 100
        HEIGHT = info.current_h - 100
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption('Papers, please (radik edition)')
        self.myfont = pygame.font.Font(None, 40)

        icon = pygame.image.load('assets/images/icon.png')
        pygame.display.set_icon(icon)

        self.background = pygame.image.load('assets/images/bg.png').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.table = pygame.image.load('assets/images/table.png').convert_alpha()

        self.person_straight = pygame.image.load('assets/images/person_1/straight.png').convert_alpha()

        self.walk_right = [
            pygame.image.load('assets/images/person_1/right.png').convert_alpha(),
            pygame.image.load('assets/images/person_1/right2.png').convert_alpha(),
            pygame.image.load('assets/images/person_1/right3.png').convert_alpha(),
        ]
        self.walk_left = [
            pygame.image.load('assets/images/person_1/left.png').convert_alpha(),
            pygame.image.load('assets/images/person_1/left2.png').convert_alpha(),
            pygame.image.load('assets/images/person_1/left3.png').convert_alpha(),
        ]

        self.player_anim_count = 0
        self.player_anim_delay = 8
        self.player_anim_timer = 0

        self.running = True
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.person_straight, (250, 150))

        


        self.screen.blit(self.table, (23, 320))
        
        pygame.display.update()
        self.clock.tick(60)

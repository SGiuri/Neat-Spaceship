import pygame

class Game:

    def __init__(self):
        self.red_h = 10
        self.yellow_h = 10
        self.yellow_bullets = []
        self.red_bullets = []

        self.red = pygame.Rect(WIDTH * 7 // 8 - SHIP_SIZE[0] // 2,
                          HEIGHT // 2 - SHIP_SIZE[1] // 2, SHIP_SIZE[1], SHIP_SIZE[0])
        self.yellow = pygame.Rect(WIDTH * 1 // 8 - SHIP_SIZE[0] // 2,
                             HEIGHT // 2 - SHIP_SIZE[1] // 2, SHIP_SIZE[1], SHIP_SIZE[0])

        self.clock = pygame.time.Clock()

        self.run = True

        pass


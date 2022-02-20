import pygame
from stuff.stuff import Ship, Border
class Game:
    fps = 60
    white = (255, 255, 255)
    width, height = 900, 500

    def __init__(self):

        self.clock = pygame.time.Clock()

        self.running = True
        self.surface = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("My Game")

        ship_width = Ship.ship_width
        ship_height = Ship.ship_height

        # becauose of ship rotation:
        self.ship_width, self.ship_height = ship_height, ship_width

        self.middle_border = Border()


        self.red_ship = Ship(Game.width // 4,
                             Game.height // 2 - self.ship_height // 2 ,
                             "red")

        self.yellow_ship = Ship(Game.width // 4 * 3,
                                Game.height // 2 - self.ship_height // 2 ,
                                "yellow")

    def run(self):
        while self.running:
            self.clock.tick(Game.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    os.exit()

            key_pressed = pygame.key.get_pressed()
            screen_resolution = Game.width, Game.height
            self.red_ship.move_ship(key_pressed, self.middle_border.get_boundaries(), screen_resolution)

            self.yellow_ship.move_ship(key_pressed, self.middle_border.get_boundaries(), screen_resolution)
            
            
            self.draw_window()

    def draw_window(self):
         self.surface.fill(Game.white)
         self.red_ship.draw(self.surface)
         self.yellow_ship.draw(self.surface)

         pygame.display.update()

if __name__ == "__main__":
    new_game = Game()
    new_game.run()
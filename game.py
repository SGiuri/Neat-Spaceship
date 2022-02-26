import pygame, os
from stuff.stuff import Ship, Border, Bullet, Bullets

class Game:
    fps = 60
    white = (255, 255, 255)
    red = (255, 0, 0)
    width, height = 900, 500

    def __init__(self):

        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen_resolution = Game.width, Game.height
        self.running = True
        self.surface = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("My Game")

        ship_width = Ship.ship_width
        ship_height = Ship.ship_height

        # becauose of ship rotation:
        self.ship_width, self.ship_height = ship_height, ship_width

        self.middle_border = Border(self.screen_resolution, 2, Game.red)


        self.left_ship = Ship(Game.width // 4,
                              Game.height // 2 - self.ship_height // 2,
                             "red", self.screen_resolution)

        self.right_ship = Ship(Game.width // 4 * 3,
                               Game.height // 2 - self.ship_height // 2,
                                "yellow", self.screen_resolution)

        self.right_bullets = Bullets()
        self.left_bullets = Bullets()

    def run(self):
        while self.running:
            self.clock.tick(Game.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RCTRL:
                        new_bullet = Bullet(self.right_ship)
                        self.right_bullets.new_bullet(new_bullet)

                    if event.key == pygame.K_LCTRL:
                        bullet = Bullet(shooter = self.left_ship)
                        self.left_bullets.new_bullet(bullet)

            key_pressed = pygame.key.get_pressed()


            self.right_bullets.handle_bullets(target = self.left_ship)
            self.left_bullets.handle_bullets(target = self.right_ship)
            self.left_ship.move_ship(key_pressed, self.middle_border.get_boundaries())

            self.right_ship.move_ship(key_pressed, self.middle_border.get_boundaries())
            
            self.draw_window()

    def draw_window(self):
         self.surface.fill(Game.white)

         self.middle_border.draw(self.surface)
         self.left_ship.draw(self.surface)
         self.right_ship.draw(self.surface)
         self.right_bullets.draw(self.surface)
         self.left_bullets.draw(self.surface)

         pygame.display.update()

if __name__ == "__main__":
    new_game = Game()
    new_game.run()
import pygame
import os

class Ship:

    ship_width, ship_height = 55, 40
    vel = 3

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

        if self.color == "red":
            self.position = "left"
        elif self.color == "yellow":
            self.position = "right"

        self.img = self.load_img()


    def load_img(self):
        file_name = 'spaceship_'+ self.color +'.png'
        ship_img = pygame.image.load(os.path.join(os.getcwd(), 'assets', file_name))
        ship_img = pygame.transform.scale(ship_img, (Ship.ship_width, Ship.ship_height))
        # red ship is the left one: rotation
        if self.position == "left":
            rotation = 90
        elif self.position == "right":
            rotation = -90

        ship_img = pygame.transform.rotate(ship_img, rotation)
        self.width = Ship.ship_height
        self.height = Ship.ship_width

        return ship_img

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
        pass

    def move_ship(self, key_pressed, middle_boarder, screen_resolution):

        top_left_x, top_left_y, bottom_right_x,bottom_right_y  = middle_boarder
        screen_width, screen_height = screen_resolution

        if self.position == "left":
            top_left_x, top_left_y, bottom_right_x, bottom_right_y = 0, \
                                                                     0, \
                                                                     top_left_x - self.width, \
                                                                     bottom_right_y

            go_left  = pygame.K_a
            go_right = pygame.K_s
            go_up    = pygame.K_w
            go_down  = pygame.K_z

        elif self.position == "right":
            top_left_x, top_left_y, bottom_right_x, bottom_right_y = bottom_right_x,\
                                                                     0, \
                                                                     screen_width - self.width, bottom_right_y

            go_left  = pygame.K_LEFT
            go_right = pygame.K_RIGHT
            go_up    = pygame.K_UP
            go_down  = pygame.K_DOWN

        if key_pressed[go_left] and self.x - Ship.vel >= top_left_x:
            self.x -= Ship.vel
        if key_pressed[go_right] and self.x + Ship.vel <= bottom_right_x:
            self.x += Ship.vel
        if key_pressed[go_up] and self.y - Ship.vel >= 0:
            self.y -= Ship.vel
        if key_pressed[go_down] and self.y + self.height + Ship.vel <= bottom_right_y:
            self.y += Ship.vel

        # print(self.x, self.y)




class Border:

    def __init__(self):

        pass

    def get_boundaries(self):
        # top_left_x, top_left_y, bottom_right_x, bottom_right_y
        return 440, 0, 460, 500
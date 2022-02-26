import os

import pygame

BLACK = (0, 0, 0)


class Ship:
    ship_width, ship_height = 55, 40
    vel = 3

    def __init__(self, x, y, color, screen_resolution):
        self.x = x
        self.y = y
        self.color = color
        self.screen_resolution = screen_resolution
        if self.color == "red":
            self.position = "left"
        elif self.color == "yellow":
            self.position = "right"

        self.img = self.load_img()

    def load_img(self):
        file_name = 'spaceship_' + self.color + '.png'
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

    def move_ship(self, key_pressed, middle_boarder):

        top_left_x, top_left_y, bottom_right_x, bottom_right_y = middle_boarder
        screen_width, screen_height = self.screen_resolution

        if self.position == "left":
            top_left_x, top_left_y, bottom_right_x, bottom_right_y = 0, \
                                                                     0, \
                                                                     top_left_x - self.width, \
                                                                     bottom_right_y

            go_left = pygame.K_a
            go_right = pygame.K_s
            go_up = pygame.K_w
            go_down = pygame.K_z

        elif self.position == "right":
            top_left_x, top_left_y, bottom_right_x, bottom_right_y = bottom_right_x, \
                                                                     0, \
                                                                     screen_width - self.width, bottom_right_y

            go_left = pygame.K_LEFT
            go_right = pygame.K_RIGHT
            go_up = pygame.K_UP
            go_down = pygame.K_DOWN

        if key_pressed[go_left] and self.x - Ship.vel >= top_left_x:
            self.x -= Ship.vel
        if key_pressed[go_right] and self.x + Ship.vel <= bottom_right_x:
            self.x += Ship.vel
        if key_pressed[go_up] and self.y - Ship.vel >= 0:
            self.y -= Ship.vel
        if key_pressed[go_down] and self.y + self.height + Ship.vel <= bottom_right_y:
            self.y += Ship.vel


        # print(self.x, self.y)

    def get_rect(self):
        rectangle = pygame.Rect(self.x, self.y,
                                self.ship_width, self.ship_width)
        return rectangle


class Border:

    def __init__(self, screen_resolution, border_width, color=BLACK):
        self.color = color

        self.border_up_left_corner_x = screen_resolution[0] // 2 - border_width // 2
        self.border_up_left_corner_y = 0
        self.border_bottom_right_corner_x = self.border_up_left_corner_x + border_width
        self.border_bottom_right_corner_y = screen_resolution[1]

        self.border = pygame.Rect(screen_resolution[0] // 2 - border_width // 2, 0,
                                  border_width, screen_resolution[1])

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.border)

    def get_boundaries(self):
        # top_left_x, top_left_y, bottom_right_x, bottom_right_y
        boundaries = (self.border_up_left_corner_x,
                      self.border_up_left_corner_y,
                      self.border_bottom_right_corner_x,

                      self.border_bottom_right_corner_y)
        return boundaries


class Bullet:

    def __init__(self, shooter, bullet_dimension = (6, 2), speed = 5):
        self.ship_shooter = shooter
        self.speed = 5


        if shooter.position == "left":
            self.speed_verse = 1
            shooter_origin_x_correction = shooter.width

        elif shooter.position == "right":
            self.speed_verse = -1
            shooter_origin_x_correction = 0

        self.color = BLACK
        self.bullet_width = bullet_dimension[0]
        self.bullet_height = bullet_dimension[1]

        self.bullet_upper_left_x = self.ship_shooter.x + shooter_origin_x_correction
        self.bullet_upper_left_y = self.ship_shooter.y + shooter.height // 2
        self.bullet_bottom_right_x = self.bullet_upper_left_x + self.bullet_width
        self.bullet = pygame.Rect(self.bullet_upper_left_x, self.bullet_upper_left_y,
                                  self.bullet_width, self.bullet_height)

    def move(self):
        self.bullet_upper_left_x += self.speed_verse * self.speed
        self.bullet = pygame.Rect(self.bullet_upper_left_x, self.bullet_upper_left_y,
                                  self.bullet_width, self.bullet_height)

    def get_rect(self):
        return self.bullet

    def on_target(self, target):
        return self.bullet.colliderect(target.get_rect())




class Bullets:

    def __init__(self):
        self.bullets = []
        pass

    def new_bullet(self, bullet):
        self.bullets.append(bullet)

    def draw(self, surface):
        for bullet in self.bullets:
            pygame.draw.rect(surface, bullet.color, bullet.get_rect())

    def move(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.bullet_upper_left_x < -10:
                self.bullets.remove(bullet)
            if bullet.bullet_bottom_right_x > 900:
                self.bullets.remove(bullet)

    def remove_bullet(self):
        for bullet in self.bullets:

            if bullet.bullet_upper_left_x < -10:
                self.bullets.remove(bullet)
            if bullet.bullet_bottom_right_x > 900:
                self.bullets.remove(bullet)



    def check_collision(self, target):
        for bullet in self.bullets:
            if bullet.on_target(target):
                self.bullets.remove(bullet)

    def handle_bullets(self, target):
        self.move()
        self.remove_bullet()
        self.check_collision(target)

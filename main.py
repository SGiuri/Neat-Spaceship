import os

import pygame

pygame.font.init()
pygame.mixer.init()
pygame.init()

HEALTH_FONT = pygame.font.SysFont("Comicsans", 40)
END_FONT = pygame.font.SysFont("Comicsans", 50)

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 2
SHIP_SIZE = (55, 40)
YELLOW_SHIP_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SHIP_IMG = pygame.transform.scale(YELLOW_SHIP_IMG, SHIP_SIZE)
YELLOW_SHIP_IMG = pygame.transform.rotate(YELLOW_SHIP_IMG, 90)
RED_SHIP_IMG = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SHIP_IMG = pygame.transform.scale(RED_SHIP_IMG, SHIP_SIZE)
RED_SHIP_IMG = pygame.transform.rotate(RED_SHIP_IMG, 270)

SPACE_IMG = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE_IMG = pygame.transform.scale(SPACE_IMG, (WIDTH, HEIGHT))

HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

MAX_N_BULLETS = 3
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)
BULLET_DIM = (10, 6)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_h, yellow_h):
    WIN.blit(SPACE_IMG, (0, 0))

    red_health_text = HEALTH_FONT.render("Health = " + str(red_h), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    yellow_health_text = HEALTH_FONT.render("Health = " + str(yellow_h), 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))

    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SHIP_IMG, (yellow.x, yellow.y))
    WIN.blit(RED_SHIP_IMG, (red.x, red.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()


def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if key_pressed[pygame.K_s] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= VEL
    if key_pressed[pygame.K_z] and yellow.y + yellow.height + VEL < HEIGHT:
        yellow.y += VEL


def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - red.width:
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y > 0:
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + red.height + VEL < HEIGHT:
        red.y += VEL


def handle_bullet(yellow_bullets, red_bullets, red, yellow):
    for bullet in yellow_bullets:
        bullet.x += 3 * VEL
        for other_bullet in red_bullets:
            if bullet.colliderect(other_bullet):
                yellow_bullets.remove(bullet)
                red_bullets.remove(other_bullet)
        if bullet.colliderect(red):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x += - 3 * VEL
        if bullet.x < 0:
            red_bullets.remove(bullet)
        if bullet.colliderect(yellow):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))


def draw_winner(game_over_text):
    g_o_text = END_FONT.render(game_over_text, 1, WHITE)
    WIN.blit(g_o_text, (WIDTH // 2 - g_o_text.get_width() // 2, 200))
    pygame.display.update()
    pygame.time.delay(1000)
    pass


def main():
    red_h = 10
    yellow_h = 10
    yellow_bullets = []
    red_bullets = []

    red = pygame.Rect(WIDTH * 7 // 8 - SHIP_SIZE[0] // 2,
                      HEIGHT // 2 - SHIP_SIZE[1] // 2, SHIP_SIZE[1], SHIP_SIZE[0])
    yellow = pygame.Rect(WIDTH * 1 // 8 - SHIP_SIZE[0] // 2,
                         HEIGHT // 2 - SHIP_SIZE[1] // 2, SHIP_SIZE[1], SHIP_SIZE[0])

    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            if event.type == RED_HIT:
                red_h -= 1
                HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_h -= 1
                HIT_SOUND.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    if len(yellow_bullets) < MAX_N_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width,
                                             yellow.y + yellow.height // 2 - BULLET_DIM[1] // 2,
                                             BULLET_DIM[0], BULLET_DIM[1])
                        SHOOT_SOUND.play()

                        yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL:
                    if len(red_bullets) < MAX_N_BULLETS:
                        bullet = pygame.Rect(red.x - BULLET_DIM[0],
                                             red.y + red.height // 2 - BULLET_DIM[1] // 2,
                                             BULLET_DIM[0], BULLET_DIM[1])
                        SHOOT_SOUND.play()
                        red_bullets.append(bullet)

        if run:
            draw_window(red, yellow,
                        red_bullets, yellow_bullets,
                        red_h, yellow_h)

        game_over_text = ""
        if red_h <= 0:
            game_over_text = "Yellow is the Winner"
        if yellow_h <= 0:
            game_over_text = "Red is the Winner"

        if game_over_text != "":
            draw_winner(game_over_text)
            main()

        handle_bullet(yellow_bullets, red_bullets, red, yellow)
        key_pressed = pygame.key.get_pressed()
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)


if __name__ == '__main__':
    main()

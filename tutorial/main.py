import pygame
import os
from config.config import window, colors, spaceship, bullet
pygame.font.init()
pygame.mixer.init()

WIDTH = window.get('WIDTH')
HEIGHT = window.get('HEIGHT')
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(window.get('TITLE'))

FPS = window.get('FPS')
VEL = window.get("VELOCITY")
BORDER = pygame.Rect(((WIDTH/2) - 5), 0, 10, HEIGHT)
BG = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'space.jpg')), (WIDTH, HEIGHT))

HEALTH_FONT = pygame.font.SysFont(window.get(
    "HEALTH_FONT_FAMILY"), window.get("HEALTH_FONT_SIZE"))
WINNER_FONT = pygame.font.SysFont(window.get(
    "WINNER_FONT_FAMILY"), window.get("WINNER_FONT_SIZE"))

FIRST_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship.png'))
FIRST_SPACESHIP = pygame.transform.scale(
    FIRST_SPACESHIP_IMAGE, (spaceship.get("WIDTH"), spaceship.get("HEIGHT")))
SECOND_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship2.png'))
SECOND_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    SECOND_SPACESHIP_IMAGE, (spaceship.get("WIDTH"), spaceship.get("HEIGHT"))), 90)

FIRST_HIT = pygame.USEREVENT + 1
SECOND_HIT = pygame.USEREVENT + 2

MAX_BULLETS = 3
BULLET_VEL = bullet.get("VELOCITY")
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'fire.wav'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'hitted.wav'))

first_bullets = []
second_bullets = []
first_health = 0
second_health = 0
first_health = spaceship.get("HEALTH")
second_health = spaceship.get("HEALTH")


def draw_window(first, second, first_bullets, second_bullets, first_health, second_health):
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, colors.get("black"), BORDER)

    first_health_text = HEALTH_FONT.render(
        "Health: " + str(first_health), 1, colors.get("white"))
    second_health_text = HEALTH_FONT.render(
        "Health: " + str(second_health), 1, colors.get("white"))
    WIN.blit(second_health_text,
             (WIDTH - second_health_text.get_width() - 10, 10))
    WIN.blit(first_health_text, (10, 10))

    WIN.blit(FIRST_SPACESHIP, (first.x, first.y))
    WIN.blit(SECOND_SPACESHIP, (second.x, second.y))

    for bullet in first_bullets:
        pygame.draw.rect(WIN, colors.get('green'), bullet)

    for bullet in second_bullets:
        pygame.draw.rect(WIN, colors.get('red'), bullet)

    pygame.display.update()


def first_handle_movement(keys_pressed, first_rect):
    if keys_pressed[pygame.K_a] and first_rect.x - VEL > 0:  # LEFT
        first_rect.x -= VEL
    # RIGHT
    if keys_pressed[pygame.K_d] and (first_rect.x + first_rect.width) + VEL < BORDER.x:
        first_rect.x += VEL
    if keys_pressed[pygame.K_w] and first_rect.y - VEL > 0:  # UP
        first_rect.y -= VEL
    # DOWN
    if keys_pressed[pygame.K_s] and (first_rect.y + first_rect.width) + VEL < HEIGHT:
        first_rect.y += VEL


def second_handle_movement(keys_pressed, second_rect):
    if keys_pressed[pygame.K_LEFT] and (second_rect.x) - VEL > BORDER.x + BORDER.width:
        second_rect.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and (second_rect.x + second_rect.width) + VEL < WIDTH:
        second_rect.x += VEL
    if keys_pressed[pygame.K_UP] and second_rect.y - VEL > 0:
        second_rect.y -= VEL
    if keys_pressed[pygame.K_DOWN] and (second_rect.y + second_rect.width) + VEL < HEIGHT:
        second_rect.y += VEL


def handle_bullets(first_bullets, second_bullets, first_sps, second_sps):
    for bullet in first_bullets:
        bullet.x += BULLET_VEL
        if second_sps.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SECOND_HIT))
            first_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            first_bullets.remove(bullet)

    for bullet in second_bullets:
        bullet.x -= BULLET_VEL
        if first_sps.colliderect(bullet):
            pygame.event.post(pygame.event.Event(FIRST_HIT))
            second_bullets.remove(bullet)
        elif bullet.x < 0:
            second_bullets.remove(bullet)


def draw_winners(text):
    draw_text = WINNER_FONT.render(text, 1, colors.get("white"))
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
             2, HEIGHT / 2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    first_health = spaceship.get("HEALTH")
    second_health = spaceship.get("HEALTH")
    first_sps = pygame.Rect(100, 300, spaceship.get(
        "WIDTH"), spaceship.get("HEIGHT"))
    second_sps = pygame.Rect(700, 300, spaceship.get(
        "WIDTH"), spaceship.get("HEIGHT"))
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(first_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        first_sps.x + first_sps.width, first_sps.y + first_sps.height/2 - 2, 10, 5)
                    first_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(second_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        second_sps.x, second_sps.y + second_sps.height/2 - 2, 10, 5)
                    second_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == FIRST_HIT:
                first_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == SECOND_HIT:
                second_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if first_health <= 0:
            winner_text = 'Right wins!'
        if second_health <= 0:
            winner_text = 'Left wins!'

        if winner_text != "":
            draw_winners(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        first_handle_movement(keys_pressed, first_sps)
        second_handle_movement(keys_pressed, second_sps)

        handle_bullets(first_bullets, second_bullets, first_sps, second_sps)

        draw_window(first_sps, second_sps, first_bullets,
                    second_bullets, first_health, second_health)

    main()


if __name__ == '__main__':
    main()

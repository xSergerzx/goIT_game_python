import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random
from os import listdir

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 800, 600

Black = 0, 0, 0
White = 255, 255, 255
Red = 255, 0, 0
Green = 0, 255, 0

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'
player_imgs = [pygame.transform.scale(pygame.image.load(
    IMGS_PATH + '/' + file).convert_alpha(), (91, 38)) for file in listdir(IMGS_PATH)]
ball = player_imgs[0]
# ball = pygame.transform.scale(pygame.image.load(
# 'player.png').convert_alpha(), (91, 38))

# ball = pygame.Surface((20, 20))
# ball.fill((White))
ball_rect = ball.get_rect()
ball_speed = 10


def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load(
        'enemy.png').convert_alpha(), (120, 40))
    # enemy = pygame.Surface((20, 20))
    # enemy.fill(Red)
    enemy_rect = pygame.Rect(
        width, random.randint(40, height), *enemy.get_size())
    enemy_speed = random.randint(3, 5)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    # bonus = pygame.Surface((20, 20))
    # bonus.fill(Green)
    bonus = pygame.transform.scale(pygame.image.load(
        'bonus.png').convert_alpha(), (133, 224))
    bonus_rect = pygame.Rect(random.randint(
        0, width-220), -bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(1, 5)
    return [bonus, bonus_rect, bonus_speed]


bg = pygame.transform.scale(pygame.image.load(
    'background.png').convert(), screen)

bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_BONUS = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_BONUS, 3000)

CREATE_ENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_ENEMY, 1500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

scores = 0
img_index = 0

enemies = []
bonuses = []

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            ball = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    # main_surface.fill((White))

    # main_surface.blit(bg, (0, 0))

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < - bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(ball, ball_rect)

    score_colour = White
    if scores > 0:
        score_colour = Green

    main_surface.blit(font.render(str(scores), True,
                      score_colour), (width-30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))

        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)
    if pressed_keys[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)
    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)
    print(len(bonuses))
    # enemy_rect = enemy_rect.move(-enemy_speed, 0)
    pygame.display.flip()

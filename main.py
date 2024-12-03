import pygame
import constants
from character import Character
from weapons import Bow

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')

clock = pygame.time.Clock()

moving_left = False
moving_right = False
moving_up = False
moving_down = False

def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    new_image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return new_image

bow_image = pygame.image.load('assets/images/weapons/bow.png').convert_alpha()
bow_image = scale_img(bow_image, constants.WEAPON_SCALE)

arrow_image = pygame.image.load('assets/images/weapons/arrow.png').convert_alpha()
arrow_image = scale_img(arrow_image, constants.WEAPON_SCALE)

mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
for mob in mob_types:
    animation_types = ["idle", "run"]
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

player = Character(100, 100, 100, mob_animations, 0)

enemy = Character(200, 300, 100, mob_animations, 1)

bow = Bow(bow_image, arrow_image)

enemy_list = [enemy]

arrow_group = pygame.sprite.Group()

running = True
while running:

    clock.tick(constants.FPS)
    screen.fill(constants.BG)

    dx = 0
    dy = 0
    if moving_left:
        dx = -constants.SPEED
    if moving_right:
        dx = constants.SPEED
    if moving_up:
        dy = -constants.SPEED
    if moving_down:
        dy = constants.SPEED

    player.move(dx, dy)

    for enemy in enemy_list:
        enemy.update()

    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)

    for enemy in enemy_list:
        enemy.draw(screen)
    for arrow in arrow_group:
        arrow.update(enemy_list)
        arrow.draw(screen)
    player.draw(screen)
    bow.draw(screen)

    print(enemy.health)

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_s:
                moving_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s:
                moving_down = False



    pygame.display.update()

pygame.quit()
import pygame
import csv
import constants
from character import Character
from weapons import Bow
from items import Item
from world import World

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')

clock = pygame.time.Clock()

level = 1
screen_scroll = [0, 0]

moving_left = False
moving_right = False
moving_up = False
moving_down = False

font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    new_image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return new_image

tile_list = []
for x in range(18):
    tile_image = pygame.image.load(f'assets/images/tiles/{x}.png').convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

heart_empty_image = scale_img(pygame.image.load('assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
heart_half_image = scale_img(pygame.image.load('assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)
heart_full_image = scale_img(pygame.image.load('assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)

coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f'assets/images/items/coin_f{x}.png').convert_alpha(), constants.ITEM_SCALE)
    coin_images.append(img)

red_potion = scale_img(pygame.image.load(f'assets/images/items/potion_red.png').convert_alpha(), constants.POTION_SCALE)

item_images = [coin_images, [red_potion]]

bow_image = scale_img(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load('assets/images/weapons/arrow.png').convert_alpha(), constants.WEAPON_SCALE)

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

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1)*20):
            screen.blit(heart_full_image, (10+ i * 50, 0))
        elif player.health % 20 > 0 and not half_heart_drawn:
            screen.blit(heart_half_image, (10+ i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty_image, (10+ i * 50, 0))

    score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images)
    score_coin.draw(screen)
    draw_text(f"LEVEL: {level}", font, constants.WHITE, constants.SCREEN_WIDTH / 2 - 50, 15)
    draw_text(f"X{player.coins}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)

world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)

with open(f'levels/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

class DamageText(pygame.sprite.Sprite):
    def __init__(self,x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

player = world.player

bow = Bow(bow_image, arrow_image)
enemy_list = world.character_list

damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

for item in world.item_list:
    item_group.add(item)

damage_text = DamageText(300, 400, 15, constants.RED)
damage_text_group.add(damage_text)

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

    screen_scroll = player.move(dx, dy, world.obstacle_tiles)

    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)

    world.update(screen_scroll)
    world.draw(screen)

    for enemy in enemy_list:
        enemy.ai(screen, player, world.obstacle_tiles, screen_scroll)
        enemy.update()

    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)
        if damage and damage_pos:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    for damage_text in damage_text_group:
        damage_text.update()
    item_group.update(screen_scroll, player)

    arrow_group.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    item_group.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    damage_text_group.draw(screen)

    draw_info()

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
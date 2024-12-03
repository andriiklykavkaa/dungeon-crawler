from random import randint

import pygame
import math

import constants


class Bow:
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = 300
        arrow = None
        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_distance = pos[0] - self.rect.center[0]
        y_distance = (pos[1] - self.rect.center[1])
        self.angle = math.degrees(math.atan2(y_distance, x_distance))



        if (pygame.mouse.get_pressed()[0] and
                not self.fired and
                (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown):
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, -self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

        return arrow


    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        surface.blit(self.image,
                     (self.rect.centerx - self.image.get_width()/2,
                      self.rect.centery - self.image.get_height()/2))


class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -math.sin(math.radians(self.angle)) * constants.ARROW_SPEED

    def update(self, enemy_list):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + randint(-5,5)
                enemy.health -= damage
                self.kill()
                break

    def draw(self, surface):
        surface.blit(self.image,
                     (self.rect.centerx - self.image.get_width() / 2,
                      self.rect.centery - self.image.get_height() / 2))
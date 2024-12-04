import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list):
        super().__init__()
        self.item_type = item_type
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, screen_scroll, player):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        if self.rect.colliderect(player.rect):
            if self.item_type == 0:
                player.coins += 1
            elif self.item_type == 1:
                player.health += 10
                if player.health >= 100:
                    player.health = 100
            self.kill()

        animation_cooldown = 150
        self.image = self.animation_list[self.frame_index]
        if (pygame.time.get_ticks() - self.update_time) >= animation_cooldown:
            self.frame_index += 1
            self.frame_index %= len(self.animation_list)
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
import pygame
from design import load_image


class Player:
    def __init__(self, sprite):
        self.catcher = sprite
        self.speed = 1
        self.count = 0
        self.pos = ()
        self.current_direction = None

    def moving(self):
        count = 20
        self.pos = (self.catcher.rect.x + self.catcher.rect.width // 2, self.catcher.rect.y)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            quit()
        if keys[pygame.K_RIGHT]:
            if self.catcher.rect.x <= 1920 - 200:
                self.catcher.rect.x += count * self.speed
                self.catcher.image = load_image('catcher_right.png')
                self.current_direction = 'right'
        if keys[pygame.K_LEFT]:
            if self.catcher.rect.x >= count + 40:
                self.catcher.rect.x -= count * self.speed
                self.catcher.image = load_image('catcher_left.png')
                self.current_direction = 'left'
        if keys[pygame.K_LSHIFT]:
            self.speed = 2.5
        else:
            self.speed = 1
        if keys[pygame.K_ESCAPE]:
            quit()

    def get_direction(self):
        return self.current_direction

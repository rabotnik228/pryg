import pygame
from design import load_image
import random


class Fruits(pygame.sprite.Sprite):
    image = load_image(f'0.png')
    image2 = load_image('busted_fruti.png')
    pygame.transform.scale(image, (50, 45))

    def __init__(self, player_in_game, player, playmode='without', speed=False, *group):
        super().__init__(*group)
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        self.forsag = speed
        if self.forsag:
            self.image = Fruits.image2
            self.tolchok = True
        else:
            self.image = Fruits.image
            self.tolchok = False
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(200, 900)
        self.rect.y = 0
        self.coordsx_of_fallen = 0
        self.catcher = player
        self.player_in_game = player_in_game
        self.count = 5
        self.on_player = False
        self.on_korzina = None
        self.count_korzina = 0
        self.za_player = False
        self.ticks = pygame.time.get_ticks()
        self.playmode = playmode

    def update(self):
        if not pygame.sprite.collide_rect(self, self.catcher):
            self.rect.y += 24
            if self.rect.y >= 1080 - 185:
                if not self.za_player:
                    nepopal = pygame.mixer.Sound('resourses/music/combobreak.mp3')
                    nepopal.set_volume(0.07)
                    nepopal.play()
                    self.za_player = True
        else:
            if self.rect.y <= 1080 - 185:
                if not self.on_player:
                    popal = pygame.mixer.Sound(f'resourses/music/{random.randrange(0, 4)}.wav')
                    popal.set_volume(0.04)
                    popal.play()
                    self.on_player = True
                    self.on_korzina = True
                    self.count_korzina += 1
                    if self.forsag:
                        self.catcher.speed = 5
                        if pygame.time.get_ticks() - self.ticks > 2000:
                            self.catcher.speed = 2.5
                            self.forsag = False
            else:
                self.rect.y += 24
                if not self.za_player:
                    nepopal = pygame.mixer.Sound('resourses/music/combobreak.mp3')
                    nepopal.set_volume(0.07)
                    nepopal.play()
                    self.za_player = True

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y


class Banana(pygame.sprite.Sprite):
    image = load_image('silent.png')

    def __init__(self, player, *group):
        super().__init__(*group)
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        self.image = Banana.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 800)
        self.rect.y = 0
        self.catcher = player
        self.count = 5
        self.on_player = False
        self.on_korzina = None
        self.count_korzina = 0

    def update(self):
        if not pygame.sprite.collide_rect(self, self.catcher):
            self.rect.y += 30
        else:
            if self.rect.y <= 1080 - 193:
                self.rect.x, self.rect.y = self.catcher.rect.x + 20, self.catcher.rect.y - 60
                if not self.on_player:
                    popal = pygame.mixer.Sound('resourses/music/spinnerbonus.wav')
                    popal.set_volume(0.04)
                    popal.play()
                    self.on_player = True
                    self.on_korzina = True
                    self.count_korzina += 1
            else:
                self.rect.y += 30

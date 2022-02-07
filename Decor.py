import pygame
import json
import Game as game


class Decor(pygame.sprite.Sprite):
    def __init__(self, element, x, y, game):
        super().__init__()

        f = open('Data/config/config.json', 'r')
        self.data = json.load(f)
        f.close()

        self.image = pygame.image.load(self.data['Decors'][element]['img']).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
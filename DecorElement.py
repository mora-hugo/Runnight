import pygame
import json
import Game as game
import Player


class DecorElement(pygame.sprite.Sprite):
    def __init__(self, element, game, x, y, width, height, speed, direction, isColliding):
        super().__init__()
        self.width = width
        self.height = height
        self.direction = direction  # x ou y : x pour horizontal et y pour vertical
        self.pos_x = x
        self.pos_y = y
        self.game = game
        self.image = pygame.transform.scale(element['img'], (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collider = isColliding
        self.speed = speed
        self.name = element['name']

    def collisionPlayer(self):
        for sprite in game.Game.get_instance().all_sprites:
            pygame.draw.rect(self.game.screen, (255, 0, 0),
                             (self.pos_x, self.pos_y, self.width, self.height))
            if self.game.player.rect.colliderect((self.pos_x, self.pos_y+25, self.width, self.height)):
                return True
        return False

    def update(self):
        if self.direction == 'x':
            self.pos_x -= self.speed
            if (self.pos_x < -1200 and self.speed > 0) or (self.pos_x > 1200 and self.speed < 0):
                self.kill()
        else:
            self.pos_y -= self.speed
            if (self.pos_y < -1200 and self.speed > 0) or (self.pos_y > 1200 and self.speed < 0):
                self.kill()

        if self.name == 'house' and self.collisionPlayer():
            self.game.planque.afficher()
            self.game.isInRun = False

        self.rect.topleft = (self.pos_x, self.pos_y)

        if not self.game.isInRun:
            self.kill()

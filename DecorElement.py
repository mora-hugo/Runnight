import pygame
import json
import Game as game
import Player


class DecorElement(pygame.sprite.Sprite):
    def __init__(self, element, game, x, y, width, height, speed, direction, isColliding, hitBoxX=None, hitBoxY=None):
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
        self.hitBoxX = hitBoxX
        self.hitBoxY = hitBoxY

    def collisionPlayer(self):
        if self.hitBoxX is not None:
            width = self.hitBoxX
        else:
            width = self.width
        if self.hitBoxY is not None:
            height = self.hitBoxY
        else:
            height = self.height
        if self.game.player.rect.colliderect((self.pos_x, self.pos_y+25, width, height)):
            self.game.player.tpPlanque = True
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

from genericpath import exists
import pygame
import json
import Game as game
import Player


class DecorElement(pygame.sprite.Sprite):
    def __init__(self, element, game, x, y, width, height, speed, direction, isColliding, hitBoxX=None, hitBoxY=None, hitBoxWidth=None, hitBoxHeight=None):
        super().__init__()

        if hitBoxX == None:
            self.hitBoxX = 0
        else:
            self.hitBoxX = hitBoxX
        if hitBoxY == None:
            self.hitBoxY = 0
        else:
            self.hitBoxY = hitBoxY
        if hitBoxWidth == None:
            self.hitBoxWidth = width
        else:
            self.hitBoxWidth = hitBoxWidth
        if hitBoxHeight == None:
            self.hitBoxHeight = height
        else:
            self.hitBoxHeight = hitBoxHeight

        self.width = width
        self.height = height
        self.direction = direction  # x ou y : x pour horizontal et y pour vertical
        self.pos_x = x
        self.pos_y = y
        self.game = game
        self.image = pygame.transform.scale(element['img'], (width, height))

        #rect image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #rect collider
        if hitBoxX == None or hitBoxY == None or hitBoxWidth == None or hitBoxHeight == None:
            self.Colliderect = self.image.get_rect()
            self.Colliderect.topleft = (x, y)
        else:
            self.Colliderect = pygame.Rect(x + hitBoxX, y + hitBoxY,hitBoxWidth ,hitBoxHeight)



        self.collider = isColliding


        self.speed = speed
        self.name = element['name']

    def collisionPlayer(self):
        if self.game.player.rect.colliderect(self.rect):
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

        self.Colliderect.topleft = (self.pos_x + self.hitBoxX, self.pos_y + self.hitBoxY)

        self.rect.topleft = (self.pos_x, self.pos_y)

        if not self.game.isInRun:
            self.kill()



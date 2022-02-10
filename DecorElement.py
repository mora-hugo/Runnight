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
        if hitBoxX == None or hitBoxY == None:
            self.Colliderect = self.image.get_rect()
            self.Colliderect.topleft = (x, y)
        else:
            self.Colliderect = pygame.Rect(x + hitBoxX, y + hitBoxY,self.hitBoxWidth ,self.hitBoxHeight)



        self.collider = isColliding


        self.speed = speed
        self.name = element['name']

    def collisionPlayer(self):
        if self.game.player.rect.colliderect(self.Colliderect):         
            return True
        return False

    def collisionDecor(self):
        for sprite in self.game.all_sprites:
            if type(sprite) is DecorElement and sprite.collider and sprite.Colliderect.colliderect(self.Colliderect):
                return True
        return False

    def update(self):
        if not self.game.monster.isStarting:
            if self.direction == 'x':
                self.pos_x -= self.speed
                if (self.pos_x < -2100 and self.speed > 0) or (self.pos_x > 1200 and self.speed < 0):
                    self.kill()
            else:
                self.pos_y -= self.speed
                if (self.pos_y < -1200 and self.speed > 0) or (self.pos_y > 1200 and self.speed < 0):
                    self.kill()

        if self.name == 'house' and self.collisionPlayer():
            self.game.player.tpPlanque = True
            self.game.planque.afficher()
            self.game.isInRun = False
            self.game.nbRun += 1
            self.game.player.multiplicateurVitesse = 1
            self.game.player.multiplicateurSaut = 1
            self.game.playground.multiplicateurVitesseCamera = 1
            if self.game.nbRun % 3 == 0:
                self.game.night = True
            else:
                self.game.night = False

        if self.name == 'money':

            if self.collisionDecor():
                self.pos_y += 100

            if self.collisionPlayer():
                self.game.player.argent +=1
                self.kill()

        self.Colliderect.topleft = (self.pos_x + self.hitBoxX, self.pos_y + self.hitBoxY)

        self.rect.topleft = (self.pos_x, self.pos_y)

        if not self.game.isInRun:
            self.kill()



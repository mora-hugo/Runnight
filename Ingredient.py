import pygame
import DecorElement
import Player


class Ingredient(pygame.sprite.Sprite):

    def __init__(self, name, element, game, x, y, speed, direction, isColliding):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction  # x ou y : x pour horizontal et y pour vertical
        self.pos_x = x
        self.pos_y = y
        self.game = game
        self.name = name
        self.image = element["img"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collider = isColliding
        self.speed = speed
        self.game = game
        self.element = element

    def isOnGround(self):
        for sprite in self.game.all_sprites:
            if type(sprite) is DecorElement.DecorElement and sprite.collider and sprite.rect.colliderect((self.rect.x, self.rect.y+self.element["height"]/2, self.element['width']-10, 20)):
                return True
        return False

    
    def collisionYdeep(self):
        for sprite in self.game.all_sprites:
            if type(sprite) is not Player and sprite.collider and sprite.rect.colliderect((self.rect.x, self.rect.y+self.element["height"]/2-10, self.element['width']-10, 20)):        
                self.pos_y -= 5

    def collisionPlayer(self):
        if self.game.player.rect.colliderect((self.pos_x, self.pos_y+25, 50, 50)):
            if self.name in self.game.player.inventory['Ingredients'].keys():
                self.game.player.inventory['Ingredients'][self.name] += 1
            else:
                self.game.player.inventory['Ingredients'][self.name] = 1
            if self.game.player.isRunning and not self.game.player.isPicking and not self.game.player.isRolling:
                self.game.player.playAnimation('pick_up',0.9)
                self.game.player.isPicking = True
            self.game.player.score += self.game.data['Ingredients'][self.name]['score']

            self.kill()

    def update(self):
        self.collisionPlayer()
        self.collisionYdeep()
        if not self.isOnGround():
            self.pos_y += 5
        if not self.game.monster.isStarting:
            if self.direction == 'x':
                self.pos_x -= self.speed
                if (self.pos_x < -1200 and self.speed > 0) or (self.pos_x > 1200 and self.speed < 0):
                    self.kill()
            else:
                self.pos_y -= self.speed
                if (self.pos_y < -1200 and self.speed > 0) or (self.pos_y > 1200 and self.speed < 0):
                    self.kill()

        self.rect.topleft = (self.pos_x, self.pos_y)

        if not self.game.isInRun:
            self.kill()

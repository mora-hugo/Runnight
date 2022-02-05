import pygame
import json


class Player(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super().__init__()

        f = open('Data/config/config.json')
        self.data = json.load(f)


        self.coordinates = coordinates
        self.hp = self.data['Player']['hp']
        self.image = pygame.Surface([20,20])
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates

        self.sprites = []
        self.currentSprite = 0
        self.animationRate = 0.1

        self.animations = {}

        self.loadAnimations()

        self.playAnimation('idle',0.1)

        self.runtostop = False

    def loadAnimations(self):
        for i in self.data['Player']['animations']:
            animPath = i['path']
            animLenght = i['lenght']
            self.animations[i['name']] = []
            for y in range(animLenght):
                self.animations[i['name']].append(pygame.image.load(animPath + str(y+1) + '.png'))

    def playAnimation(self, animation, rate):
        self.sprites = self.animations[animation]
        self.animationRate = rate
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = self.coordinates
    
    def action(self, event):
        if event.type == pygame.KEYDOWN:
            self.playAnimation('fastrun',0.4)
        if event.type == pygame.KEYUP:
            self.playAnimation('runtostop',0.4)
            self.runtostop = True

    def update(self):
        self.currentSprite += self.animationRate

        if self.currentSprite >= len(self.sprites):
            if self.runtostop == True:
                self.playAnimation('idle',0.1)
                self.runtostop = False
            self.currentSprite = 0

        self.image = self.sprites[int(self.currentSprite)]




        
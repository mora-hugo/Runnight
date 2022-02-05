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

        self.currentAnimation = 'idle'

        self.playAnimation('idle',0.1)

    def playAnimation(self, animation, rate):
        self.currentAnimation = animation
        self.animationRate = rate
        jsonAnimElem = self.data['Player']['animations'][animation]
        animPath = jsonAnimElem['path']
        animLenght = jsonAnimElem['lenght']
        self.sprites = []
        self.currentSprite = 0
        for i in range(animLenght):
           self.sprites.append(pygame.image.load(animPath + str(i+1) + '.png'))

        
        self.image = self.sprites[self.currentSprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = self.coordinates
    
    def action(self, event):
        if event.type == pygame.KEYDOWN:
            self.playAnimation('fastrun',0.4)
        if event.type == pygame.KEYUP:
            self.playAnimation('idle',0.1)

    def update(self):
        self.currentSprite += self.animationRate

        if self.currentSprite >= len(self.sprites):
            self.currentSprite = 0

        self.image = self.sprites[int(self.currentSprite)]




        
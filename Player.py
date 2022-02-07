import pygame
import json
import Game as game


class Player(pygame.sprite.Sprite):
    def __init__(self, coordinates,game):
        super().__init__()


        self.updateJson()

        self.coordinates = coordinates
        self.hp = self.data['Player']['hp']
        self.image = pygame.Surface([20,20])
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates
        self.playerScale = (150,275)

        self.sprites = []
        self.currentSprite = 0
        self.animationRate = 0.1

        self.speed_x = self.data['Player']["speed_x"]
        self.speed_y = self.data['Player']["speed_y"]

        self.animations = {}

        self.loadAnimations()

        self.isRunning = False
        self.direction = 'left'

        self.playAnimation('idle',0.4)

        self.runtostop = False
        self.stoptorun = False

        self.jeu = game #Creation instance jeu

    def loadAnimations(self):
        for i in self.data['Player']['animations']:
            animPath = i['path']
            animLenght = i['lenght']
            self.animations[i['name']] = []
            for y in range(animLenght):
                img = pygame.image.load(animPath + str(y+1) + '.png').convert_alpha()
                img = pygame.transform.scale(img,self.playerScale)
                self.animations[i['name']].append(img)

    def playAnimation(self, animation, rate):
        self.sprites = self.animations[animation]
        self.animationRate = rate
        self.currentSprite = 0
        #self.image = self.sprites[self.currentSprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = self.coordinates

    def action(self,event):
        if self.jeu.key_pressed[self.data['Bindings']['left']] == True:
            if self.isRunning == False:
                self.playAnimation('fastrun',0.9)
                self.isRunning = True
                self.runtostop = False
                self.direction = 'left'

        if self.jeu.key_pressed[self.data['Bindings']['right']] == True:
            if self.isRunning == False:
                self.playAnimation('fastrun',0.9)
                self.isRunning = True
                self.runtostop = False
                self.direction = 'right'

        if event.type == pygame.KEYUP:
            
            if event.key == self.data['Bindings']['right'] or event.key == self.data['Bindings']['left']:
                self.playAnimation('runtostop',0.9)
                self.runtostop = True
                self.isRunning = False

    def update(self):
        self.currentSprite += self.animationRate

        if self.isRunning == True:
            if self.direction == 'left':
                self.speed_x = self.data['Player']["speed_x"]
                y = list(self.coordinates)
                y[0] -= self.speed_x
                self.coordinates = tuple(y)

            if self.direction == 'right':
                self.speed_x = self.data['Player']["speed_x"]
                y = list(self.coordinates)
                y[0] += self.speed_x
                self.coordinates = tuple(y)

        if self.currentSprite >= len(self.sprites):
            if self.runtostop == True:
                if self.isRunning == False:
                    self.playAnimation('idle',0.4)
                self.runtostop = False
            elif self.stoptorun == True:
                self.playAnimation('fastrun',0.9)
                self.stoptorun = False
            self.currentSprite = 0

        if self.direction == 'right':
            self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)
        if self.direction == 'left':
            self.image = self.sprites[int(self.currentSprite)]

        if self.runtostop == True:
            
            if self.speed_x > 0:
                self.speed_x -=0.4
            if self.direction == 'left':
                y = list(self.coordinates)
                y[0] -= self.speed_x
                self.coordinates = tuple(y)

            if self.direction == 'right':
                y = list(self.coordinates)
                y[0] += self.speed_x
                self.coordinates = tuple(y)
            
            

        
        self.rect.topleft = self.coordinates



    def updateJson(self):
        f = open('Data/config/config.json',"r")
        self.data = json.load(f)
        f.close()

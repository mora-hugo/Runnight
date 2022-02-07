import pygame
import json
import Game as game


class Player(pygame.sprite.Sprite):
    def __init__(self, coordinates,game):
        super().__init__()


        self.updateJson()

        self.coordinates = coordinates
        self.hp = self.data['Player']['hp']
        self.image = pygame.Surface([1,1])
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates
        self.playerScale = (150,275)

        self.collider = True

        self.sprites = []
        self.currentSprite = 0
        self.animationRate = 0.1

        self.speed_x = self.data['Player']["speed_x"]
        self.speed_y = self.data['Player']["speed_y"]
        self.gravity = self.data['Player']["gravity"]

        self.animations = {}

        self.loadAnimations()

        self.isRunning = False
        self.direction = 'left'

        self.isJumping = False
        self.isFlying = False

        self.isLanding = False

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

        self.rect = self.image.get_rect()
        self.rect.topleft = self.coordinates

    def setAnimation(self, animation, rate):
        self.sprites = self.animations[animation]
        if self.currentSprite >= len(self.sprites):
            self.currentSprite = 0
        self.animationRate = rate
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coordinates

    def isOnGround(self):
        for sprite in game.Game.get_instance().all_sprites:
            if type(sprite) is not Player and sprite.collider and sprite.rect.colliderect((self.rect.x , self.rect.y + 1,self.data['Player']['width'],self.data['Player']['height'])):
                
                return True
        return False

    def collisionY(self,nouvPos):
        for sprite in game.Game.get_instance().all_sprites:
            if type(sprite) is not Player and sprite.collider and sprite.rect.colliderect((self.rect.x , self.rect.y + self.speed_y,self.data['Player']['width'],self.data['Player']['height'])):
                self.speed_y = 0
                nouvPos[1] -= 1
                self.isFlying = False
                

    def collisionX(self,direction):
        for sprite in game.Game.get_instance().all_sprites:
            if direction == "left":
                if type(sprite) is not Player and sprite.collider and sprite.rect.colliderect((self.rect.left, self.rect.y-10 ,self.data['Player']['width'],self.data['Player']['height'])):
                    return True
            else:
                if type(sprite) is not Player and sprite.collider and sprite.rect.colliderect((self.rect.x+self.data['Player']['width']/2+5, self.rect.y-10 ,self.data['Player']['width'],self.data['Player']['height'])):
                    return True
        return False
                

    def action(self,event):
        if self.jeu.key_pressed[self.data['Bindings']['left']] == True:
            if self.isRunning == False:
                #self.playAnimation('fastrun',0.9)
                self.isRunning = True
                self.runtostop = False
                self.direction = 'left'

        if self.jeu.key_pressed[self.data['Bindings']['right']] == True:
            if self.isRunning == False:
                #self.playAnimation('fastrun',0.9)
                self.isRunning = True
                self.runtostop = False
                self.direction = 'right'

        if self.jeu.key_pressed[self.data['Bindings']['jump']] == True:
            if self.isJumping == False and self.speed_y == 0:
                self.playAnimation('jump',1)
                self.isJumping = True
                self.isRunning = False
                self.runtostop = False

        if event.type == pygame.KEYUP:
            
            if event.key == self.data['Bindings']['right'] or event.key == self.data['Bindings']['left']:
                if not self.isLanding and self.isJumping == False and self.speed_y == 0:
                    self.playAnimation('runtostop',0.9)
                    self.runtostop = True
                self.isRunning = False

    def update(self):
        if self.jeu.currentMenu == "gameMenu":
            #graviter
            nouvPos = list(self.coordinates)

            if not self.isOnGround() and not self.isJumping:   
                self.isFlying = True      
                nouvPos[1] += self.speed_y
                self.coordinates = tuple(nouvPos)

                       

            self.currentSprite += self.animationRate

            if self.speed_y == 0:

                if self.isFlying == True:
                    self.isLanding = True
                    self.playAnimation('runtostop',0.9)
                    self.isFlying = False

                

                if self.isRunning == True:
                    if not self.isJumping:
                        self.setAnimation('fastrun',0.9)
                        self.speed_x = self.data['Player']["speed_x"]

                    elif self.speed_x > 0:
                        self.speed_x -= 0.1
                    if self.direction == 'left' and not self.collisionX('left'):    
                        nouvPos[0] -= self.speed_x
                    if self.direction == 'right' and not self.collisionX('right'):
                        nouvPos[0] += self.speed_x

                elif not self.isLanding and not self.runtostop and not self.stoptorun and not self.isJumping:
                    self.setAnimation('idle',0.4)

                if self.currentSprite >= len(self.sprites):
                    if self.runtostop == True:
                        if self.isRunning == False:
                            self.playAnimation('idle',0.4)
                        self.runtostop = False
                    if self.stoptorun == True:
                        self.playAnimation('fastrun',0.9)
                        self.stoptorun = False
                    if self.isLanding == True:
                        self.playAnimation('idle',0.4)
                        self.isLanding = False
                    self.currentSprite = 0
                    
                

                if self.runtostop == True: 
                    
                    if self.speed_x > 0:
                        self.speed_x -=0.4
                    if self.direction == 'left':
                        if not self.collisionX('left'):
                            nouvPos[0] -= self.speed_x

                    if self.direction == 'right':
                        if not self.collisionX('right'):
                            nouvPos[0] += self.speed_x

                    

                if self.direction == 'right':
                    self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)
                if self.direction == 'left':
                    self.image = self.sprites[int(self.currentSprite)]

                if self.isJumping == True:
                    self.speed_y = 10
                    nouvPos[1] -= self.speed_y
                    

            elif self.speed_y != 0:

                if self.isJumping == True:
                    nouvPos[1]-= self.speed_y #(-0.001*(y[0]*y[0]))
                    if self.speed_y > 0.5:
                        self.speed_y -= 0.5
                        
                    else:
                        self.speed_y = 0.1
                        self.isJumping = False
                        
                    
                    if not self.currentSprite >= len(self.sprites):
                        self.playAnimation('jumploop',3)

                    if self.collisionX('left') or self.collisionX('right'):
                        self.speed_y = 0.1
                        self.isJumping = False
                    

                else:    
                    self.setAnimation('jumploop',3)
                    self.speed_y +=0.2
                    nouvPos[1] += self.speed_y

                if self.direction == 'right':
                    self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)
                    if not self.collisionX('right'):
                        nouvPos[0] += self.speed_x
                if self.direction == 'left':
                    self.image = self.sprites[int(self.currentSprite)]
                    if not self.collisionX('left'):
                        nouvPos[0] -= self.speed_x

                    
                    
                        

            if self.collisionX('left'):
                self.isJumping = False
                self.isFlying = False


            if self.collisionX('right'):
                self.isJumping = False
                self.isFlying = False
            
            
            
            self.collisionY(nouvPos)
            self.coordinates = tuple(nouvPos)
            self.rect.topleft = self.coordinates



    def updateJson(self):
        f = open('Data/config/config.json',"r")
        self.data = json.load(f)
        f.close()

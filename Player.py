from msilib.schema import Class
from random import randint
from select import select
import pygame
import json
from DecorElement import DecorElement
import Sound
import Game as game
import time
import Bouton
import InventoryItem
import os
import Classement
class Player(pygame.sprite.Sprite):
    def __init__(self, coordinates, game):
        super().__init__()
        self.sound = Sound.Sound()
        self.game = game
        self.lastUpdatedFrame = time.time()
        self.updateJson()
        self.fonts = pygame.font.Font(self.data["Font"]["base"], 60)
        self.coordinates = coordinates
        self.hp = self.data['Player']['hp']
        self.image = pygame.Surface([1, 1])
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates
        self.playerScale = (150, 275)

        self.collider = True

        self.sprites = []
        self.currentSprite = 0
        self.animationRate = 0.1

        self.speed_x = self.data['Player']["speed_x"]
        self.speed_y = self.data['Player']["speed_y"]
        self.gravity = self.data['Player']["gravity"]
        self.jumpForce = self.data['Player']["jumpForce"]

        self.animations = {}

        self.loadAnimations()

        self.isRunning = False
        self.direction = 'right'

        self.isJumping = False
        self.isFlying = False
        self.isTurning = False
        self.isTurningRun = False
        self.isRiding = False
        self.isFallingSlow = False
        self.isPicking = False
        self.isRolling = False
        self.multiplicateurVitesse = 1
        self.multiplicateurSaut = 1

        self.multiplicateurVitesseDefinitif = 1
        self.multiplicateurSautDefinitif = 1
        self.tpPlanque = False
        self.tpRun = False

        self.gameOverWait = False
        self.gameOverDelay = None

        self.isFallingHard = False
        self.hardLandingBonus = 0
        self.isLanding = False
        self.bonusRiding = 0
        self.playAnimation('idle', 0.4)

        self.runtostop = False
        self.stoptorun = False

        self.jeu = game  # Creation instance jeu
        self.inventory = {
            "Ingredients" : {
                
            },
            "Plats" : {

            }
        }
        self.argent = 0
        self.score = 0

        self.background_image = pygame.image.load(
            self.data["Background_images"]["gameOver"]).convert()

    def loadAnimations(self):
        for i in self.data['Player']['animations']:
            animPath = i['path']
            animLenght = i['lenght']
            self.animations[i['name']] = []
            for y in range(animLenght):
                img = pygame.image.load(
                    animPath + str(y+1) + '.png').convert_alpha()
                img = pygame.transform.scale(img, self.playerScale)
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
            if type(sprite) is DecorElement and sprite.collider and sprite.Colliderect.colliderect((self.rect.x+39, self.rect.y+self.data['Player']['height']-10, self.data['Player']['width']-10, 20)):

                return True
        return False

    def collisionY(self):
        for sprite in game.Game.get_instance().all_sprites:
            if type(sprite) is DecorElement and sprite.collider and sprite.Colliderect.colliderect((self.rect.x+39, self.rect.y+self.data['Player']['height']-10, self.data['Player']['width']-10, 20)):
                self.speed_y = 0

    def collisionYdeep(self, nouvPos):
        for sprite in game.Game.get_instance().all_sprites:
            if type(sprite) is DecorElement and sprite.collider and sprite.Colliderect.colliderect((self.rect.x+37, self.rect.y+self.data['Player']['height']-20, self.data['Player']['width']-8, 20)):
                self.speed_y = 0
                if self.isRiding:
                    nouvPos[1] -= 5+self.bonusRiding
                else:
                    nouvPos[1] -= 1
                    nouvPos[0] += 1

    def collisionXup(self, direction):
        for sprite in game.Game.get_instance().all_sprites:
            if direction == "left":
                if type(sprite) is DecorElement and sprite.collider and sprite.Colliderect.colliderect((self.rect.left, self.rect.y+20 ,self.data['Player']['width']/2,self.data['Player']['height']/2.5)):
                    return True
            else:
                if type(sprite) is DecorElement and sprite.collider and sprite.Colliderect.colliderect((self.rect.left+120, self.rect.y+20 ,self.data['Player']['width']/2,self.data['Player']['height']/2.5)):
                    return True
        return False

    def collisionX(self, direction):
        for sprite in game.Game.get_instance().all_sprites:
            if direction == "left":
                if type(sprite) is DecorElement and sprite.collider and sprite.Colliderect.colliderect((self.rect.left+30, self.rect.y-20, self.data['Player']['width']/2, self.data['Player']['height'])):
                    return True
            else:
                if type(sprite) is DecorElement and sprite.collider and sprite.Colliderect.colliderect((self.rect.x+80, self.rect.y-20, self.data['Player']['width']/2, self.data['Player']['height'])):
                    return True
        return False

    def action(self,event):

        if self.jeu.currentMenu == "gameMenu":
            if self.jeu.key_pressed[self.data['Bindings']['pause']] == True:
                    self.pause()

            if self.jeu.key_pressed[self.data['Bindings']['left']] == True and not self.isFallingHard:
                if (time.time() >= self.lastUpdatedFrame + 0.6): 
                    self.lastUpdatedFrame = time.time()
                    self.sound.playSound("run",0.03) 

                if not self.collisionX('left'):
                    if self.direction == 'right' and self.speed_y == 0:
                        if self.isRunning == False:
                            self.playAnimation('turn',5)
                            self.isTurning = True
                        else:              
                            self.playAnimation('turn_run',1.2)  
                            self.isTurningRun = True   
                    self.direction = 'left'  
                    self.isRunning = True
                    self.runtostop = False
                    

            if self.jeu.key_pressed[self.data['Bindings']['right']] == True and not self.isFallingHard:  
        
                if (time.time() >= self.lastUpdatedFrame + 0.6): 
                    self.lastUpdatedFrame = time.time()
                    self.sound.playSound("run",0.03)       

                
                if not self.collisionX('right'):
                    if self.direction == 'left' and self.speed_y == 0 and not self.isRiding and not self.isLanding:
                        if self.isRunning == False:            
                            self.playAnimation('turn',5)
                            self.isTurning = True
                        else:             
                            self.playAnimation('turn_run',1.2)  
                            self.isTurningRun = True 
                    self.direction = 'right'   
                    self.isRunning = True
                    self.runtostop = False

            if self.jeu.key_pressed[self.data['Bindings']['jump']] == True and not self.isRiding and self.game.isInRun and not self.isFallingHard and not self.isJumping and not self.isFlying:
                self.sound.StopSound()
                
                if (time.time() >= self.lastUpdatedFrame): 
                    self.lastUpdatedFrame = time.time()
                    if (randint(1,1000) == 5):
                        self.sound.playSound("jumpProot",0.1)
                    else:
                        self.sound.playSound("jump",0.1)
                
                if self.direction == 'left':
                    if not self.collisionXup('left') and self.collisionX('left'):
                        self.runtostop = False
                        self.isLanding = False
                        self.playAnimation('jump_ride',1.5*(self.bonusRiding+5)/5)
                        self.isRiding = True
                        
                    elif self.isJumping == False and self.speed_y == 0:
                        self.playAnimation('jumploop',3)
                        self.isJumping = True
                        self.runtostop = False
                else:
                    if not self.collisionXup('right') and self.collisionX('right'):
                        self.runtostop = False
                        self.isLanding = False
                        self.playAnimation('jump_ride',1.5*(self.bonusRiding+5)/5)
                        self.isRiding = True

                    elif self.isJumping == False and self.speed_y == 0:
                        self.playAnimation('jumploop',3)
                        self.isJumping = True
                        self.runtostop = False
            

            if self.jeu.key_pressed[self.data['Bindings']['roll']] == True and self.isFallingHard and self.currentSprite <= 20 and not self.isRolling:
                self.isFallingHard = False
                self.playAnimation('roll',1.5)
                self.isRolling = True

            if event.type == pygame.KEYUP:                

                if (event.key == self.data['Bindings']['right'] and not self.jeu.key_pressed[self.data['Bindings']['left']]) or (event.key == self.data['Bindings']['left'] and not self.jeu.key_pressed[self.data['Bindings']['right']]):
                    if not self.isLanding and self.isJumping == False and self.speed_y == 0 and self.isRunning and not self.isTurning and not self.isTurningRun:
                        if not self.isFallingHard and not self.isRolling:
                            self.playAnimation('runtostop',0.9)
                            if not self.isRiding:
                                self.runtostop = True
                    self.isRunning = False

    def update_background(self):    
        game.Game.get_instance().screen.blit(self.background_image, (0, 0))

    def GameOver(self):
        if  self.game.menu.classement.bddScore is not False:
            self.game.menu.classement.bddScore.addScore(os.environ.get('USERNAME'),self.score,self.game.nbRun)
            self.game.all_sprites.remove(self.game.menu.classement.scores)
            #self.game.menu.update_background()
        self.sound.playSound("death",0.09)
        self.sound.StopGroar()
        pygame.mixer.music.stop()
        self.game.playground.update_background()
        self.game.currentMenu = "gameOver"
        self.rect.topleft = (0,-500)
        
    def pause(self):
        loop = 1
        size = (1024,768)
        BLACK = (0, 0, 0)
        red_image = pygame.Surface(size)
        red_image.set_alpha(80)
        pygame.draw.rect(red_image, BLACK, red_image.get_rect(), 10)
        text1 = self.fonts.render("PAUSED", 450, 150)
        text2 = self.fonts.render("Press escape to continue", 400, 250)
        self.game.screen.blit(red_image, (0, 0))
        self.game.screen.blit(text1, (445, 150))
        self.game.screen.blit(text2, (280, 250))
        while loop:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loop = 0
                        
            pygame.display.update()
            

    def update(self):
        if self.jeu.currentMenu == "gameMenu":

            self.currentSprite += self.animationRate

            nouvPos = list(self.coordinates)

            if self.jeu.isInRun:

                ############################## EN RUN ######################################

                if self.tpRun == True:
                    nouvPos[0] = 500
                    nouvPos[1] = 350
                    self.direction = 'right'
                    self.tpRun = False

                if self.speed_y == 0:

                    if self.isFlying == True:
                        if not self.isFallingHard:
                            if not self.isRunning:
                                self.isLanding = True
                                self.playAnimation('runtostop',0.9)
                        elif not self.isFallingSlow:
                            pass
                        else:
                            self.sound.playSound("crash",0.15)
                            self.playAnimation('hard_landing',1+self.hardLandingBonus/10)
                        self.runtostop = False        
                        self.isFlying = False

                    

                    if self.isRunning == True and not self.isTurningRun and not self.isFallingHard and not self.isRiding and not ((self.collisionX('left') and self.direction == 'left') or (self.collisionX('right') and self.direction == 'right')):
                        
                        if not  self.isTurning and not self.isJumping and not self.isPicking and not self.isRolling:
                            self.setAnimation('fastrun',0.9)
                            self.score += 1
                        self.speed_x = self.data['Player']["speed_x"]*self.multiplicateurVitesse*self.multiplicateurVitesseDefinitif
                        if self.isLanding == True:
                            self.isLanding = False

                        elif self.speed_x > 0:
                            self.speed_x -= 0.1

                        if self.direction == 'left' and not self.collisionX('left'):    
                            nouvPos[0] -= self.speed_x
                        if self.direction == 'right' and not self.collisionX('right'):
                            nouvPos[0] += self.speed_x

                    elif not self.isLanding and not self.runtostop and not self.stoptorun and not self.isJumping and not self.isTurning and not self.isTurningRun and not self.isFallingHard and not self.isRiding and not self.isPicking and not self.isRolling:
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
                        if self.isTurning == True:
                            self.playAnimation('idle',0.4)
                        self.isTurning = False
                        #if self.isTurningRun == True:                       
                        self.isTurningRun = False

                        if self.isFallingHard == True:
                            self.playAnimation('idle',0.4)
                        self.isFallingHard = False
                        if self.isRiding == True:
                            self.playAnimation('idle',0.4)
                        self.isRiding = False
                        #if self.isPicking == True:
                        self.isPicking = False
                        if self.isRolling == True:
                            self.score += 5000
                        self.isRolling = False
                        self.currentSprite = 0
                        
                    

                    if self.runtostop == True or self.isLanding == True or self.isRolling and self.isRunning == False: 
                        
                        if self.speed_x > 0:
                            self.speed_x -=0.4
                        if self.direction == 'left':
                            if not self.collisionX('left'):
                                nouvPos[0] -= self.speed_x

                        if self.direction == 'right':
                            if not self.collisionX('right'):
                                nouvPos[0] += self.speed_x

                    if self.isRiding:
                        if self.direction == 'left':
                            
                            nouvPos[0] -= 2

                        if self.direction == 'right':
                            
                            nouvPos[0] += 2
                    

                        

                    if self.direction == 'right':
                        if self.isTurningRun == False and self.isTurning == False:
                            self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)
                        else:
                            self.image = self.sprites[int(self.currentSprite)]
                        
                    if self.direction == 'left':
                        if self.isTurningRun == False and self.isTurning == False:               
                            self.image = self.sprites[int(self.currentSprite)]
                        else:
                            self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)
                        

                    if self.isJumping == True:
                        self.speed_y = self.jumpForce*self.multiplicateurSaut*self.multiplicateurSautDefinitif
                        nouvPos[1] -= self.speed_y
                        
                        

                elif self.speed_y != 0:                   
                    self.isTurning = False
                    self.isTurningRun = False
                    self.isPicking = False
                    if self.isJumping == True:

                        if self.isRunning:
                            self.speed_x = (self.data['Player']["speed_x"]*self.multiplicateurVitesse*self.multiplicateurVitesseDefinitif)/1.5
                            if self.direction == 'left' and not self.collisionX('left'):    
                                nouvPos[0] -= self.speed_x
                            if self.direction == 'right' and not self.collisionX('right'):
                                nouvPos[0] += self.speed_x
                        
                        nouvPos[1]-= self.speed_y 
                        if self.speed_y > 0.5:
                            self.speed_y -= 0.5
                            
                        else:
                            self.speed_y = 0.1
                            self.isJumping = False
                            
                        
                        if not self.currentSprite >= len(self.sprites):
                            self.playAnimation('jumploop',3)

                        

                    else:    
                        if (time.time() >= self.lastUpdatedFrame+0.3): 
                            self.lastUpdatedFrame = time.time()
                            self.sound.playSound("fall",0.01)
                        
                        self.setAnimation('jumploop',3)
                        self.speed_y +=0.2
                        nouvPos[1] += self.speed_y

                        if self.speed_y >= 10:
                            self.isFallingHard = True
                        if self.speed_y <= 1.5:
                            self.isFallingSlow = True

                    if self.direction == 'right':
                        self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)
                        if not self.collisionX('right'):
                            nouvPos[0] += self.speed_x*self.multiplicateurSaut*self.multiplicateurSautDefinitif
                    if self.direction == 'left':
                        self.image = self.sprites[int(self.currentSprite)]
                        if not self.collisionX('left'):
                            nouvPos[0] -= self.speed_x*self.multiplicateurSaut*self.multiplicateurSautDefinitif



                if not self.isOnGround() and not self.isJumping and not self.isFlying:   
                    self.isFlying = True      
                    self.speed_y = 0.1
                    
                
                
                self.collisionYdeep(nouvPos)
                self.collisionY()

                if not self.game.monster.isStarting:
                    nouvPos[0] -= self.game.playground.speed
                    

                #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left, self.rect.y+20 ,self.data['Player']['width']/2,self.data['Player']['height']/2.5))
                #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+120, self.rect.y+20 ,self.data['Player']['width']/2,self.data['Player']['height']/2.5))
                #pygame.draw.rect(self.game.screen,(255,255,255),(self.rect.x+39 , self.rect.y+self.data['Player']['height'],self.data['Player']['width']-10,20))
                #pygame.draw.rect(self.game.screen,(0,0,255),(self.rect.x+80, self.rect.y-10 ,self.data['Player']['width']/2,self.data['Player']['height']))

            else:

                ############################## A LA PLANQUE ######################################

                if self.tpPlanque == True:
                    nouvPos[0] = 500
                    self.tpPlanque = False
                
                self.speed_y == 0
                self.isFlying = False
                self.isJumping = False
                self.isLanding = False
                self.isRiding = False
                self.isFallingHard = False
                self.isFallingSlow = False
                self.isPicking = False

                if self.isRunning == True and not self.isTurningRun :
                    if not  self.isTurning:
                        self.setAnimation('fastrun',0.9)
                        self.speed_x = self.data['Player']["speed_x"]
                    elif self.speed_x > 0:
                        self.speed_x -= 0.1
                    if self.direction == 'left' and nouvPos[0] >=10 :    
                        nouvPos[0] -= self.speed_x
                    if self.direction == 'right':
                        nouvPos[0] += self.speed_x
                elif not self.runtostop and not self.isTurning and not self.isTurningRun:
                    self.setAnimation('idle',0.4)

                if self.runtostop == True: 
                        
                        if self.speed_x > 0:
                            self.speed_x -=0.4
                        if self.direction == 'left':
                            if not self.collisionX('left'):
                                nouvPos[0] -= self.speed_x

                        if self.direction == 'right':
                            if not self.collisionX('right'):
                                nouvPos[0] += self.speed_x

                if self.currentSprite >= len(self.sprites):
                        if self.runtostop == True:
                            if self.isRunning == False:
                                self.playAnimation('idle',0.4)
                            self.runtostop = False
                        if self.isTurning == True:
                            self.playAnimation('idle',0.4)
                            self.isTurning = False
                        if self.isTurningRun == True:                       
                            self.isTurningRun = False

                        self.currentSprite = 0

                if self.direction == 'right':
                        if self.isTurningRun == False and self.isTurning == False:
                            self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)
                        else:
                            self.image = self.sprites[int(self.currentSprite)]
                        
                if self.direction == 'left':
                    if self.isTurningRun == False and self.isTurning == False:               
                        self.image = self.sprites[int(self.currentSprite)]
                    else:
                        self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)

                if nouvPos[0] >= 1000:
                    self.game.startRun() #lancement du prochain run!

                
                nouvPos[1] = 530
            self.coordinates = tuple(nouvPos)
            self.rect.topleft = self.coordinates   
            if nouvPos[0] <= -200 or nouvPos[1] >= 1000:
                self.GameOver()
        elif self.jeu.currentMenu == "gameOver":   
            self.update_background()
            if pygame.mouse.get_pressed()[0]:
                if self.gameOverWait == False:
                    self.gameOverDelay = time.time()
                    self.gameOverWait = True
                    
            if self.gameOverDelay != None:
                if time.time() >= self.gameOverDelay + 0.1:
                    self.sound.playMusic("menu",None,0.03)
                    self.jeu.currentMenu = "mainMenu"
                    self.gameOverWait = False
                    self.gameOverDelay = None

    def updateJson(self):
        f = open('Data/config/config.json', "r")
        self.data = json.load(f)
        f.close()

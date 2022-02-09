from random import randint
import pygame
import Bouton as bouton
import Game as game
import json
import Sound
import time

class Playground:
    def __init__(self, screen, game):
        self.game = game
        self.decor = game.decor
        self.music = Sound.Sound()
        # Tableaux contenant tous les boutons du menu
        self.echapMenuButtons = pygame.sprite.Group()

        # Ajout des boutons pour le menu principal
        # self.text = fonction associe au bouton
        self.echapMenuButtons.add(
            bouton.Bouton(10, 10, "Reprendre", self.test))
        self.echapMenuButtons.add(bouton.Bouton(
            10, 100, "Retour menu", self.test))
        self.echapMenuButtons.add(bouton.Bouton(10, 300, "Quitter", self.test))

        self.lastClickedButton = None
        self.currentMenu = self.echapMenuButtons

        # Lecture du json pour les data
        file = open('Data/config/config.json', "r")
        self.data = json.load(file)
        file.close()

        #Chargements plats
        self.plats = self.game.data["Plats"]
        for plats in self.plats:
            self.plats[plats]["img"] = pygame.image.load(self.plats[plats]["img"]).convert_alpha()
            self.plats[plats]["img"] = pygame.transform.scale(self.plats[plats]["img"],(self.plats[plats]["width"],self.plats[plats]["height"]))
        # Background de bg
        self.background_image = pygame.image.load(
            self.data["Background_images"]["gameMenu"]).convert()  # Chargement background

        self.ground = pygame.Rect(0, 550, 1024, 500)
        pygame.draw.rect(screen, (255, 255, 255), self.ground)
        # Creation images ingrédients
        self.imgIngredients = {}
        

    # Affiche les elements du menu
        
    def afficher(self, group_menu=None):
        if group_menu == None:  # si pas de menu rentré, alors mettre le menu de base
            group_menu = self.echapMenuButtons
        jeu = game.Game.get_instance()
        jeu.all_sprites.add(group_menu)

    # Cache les elements du menu
    def cacher(self, group_menu=None):
        if group_menu == None:  # si pas de menu rentré, alors mettre le menu de base
            group_menu = self.echapMenuButtons
        jeu = game.Game.get_instance()
        jeu.all_sprites.remove(group_menu)
        self.update_background()

    # Switch to gameMenu

    def gameMenu(self):
        self.cacher(self.currentMenu)
        self.afficher(self.echapMenuButtons)
        self.currentMenu = self.echapMenuButtons

    def goToGame(self):
        self.cacher(self.currentMenu)
        self.currentMenu = None

    def update_background(self):
        game.Game.get_instance().screen.blit(self.background_image, (0, 0))

    def generateWorld(self, night, nbRun):
        biome = 'ville'
        if (randint(0,1) == 1):
            biome = 'forest'
        
        self.music.playMusic(biome,"f", 0.09)
        speed = nbRun + 1
        runLenght = nbRun*1.5+20
        x = 0
        treesx = 0
        # fond
        if not night:
            self.decor.spawnDecor('moon', 0, 0, self.data['Settings']['WIDTH'], self.data['Settings']['HEIGHT'], 0, 'x', False)
        else:
            self.decor.spawnDecor('moon', 0, 0, self.data['Settings']['WIDTH'], self.data['Settings']['HEIGHT'], 0, 'x', False)

        for i in range(0, int(runLenght)):
            if biome == 'foret':
                if not night:
                   
                    self.decor.spawnDecor(
                        'foret_jour', x, -200, 1200, 1000, speed/5, 'x', False)
                else:
                    self.decor.spawnDecor(
                        'moon', x, 0, 1200, 1000, speed/5, 'x', False)
                    self.decor.spawnDecor(
                        'foret_nuit', x, -200, 1200, 1000, speed/5, 'x', False)
            else :
                if not night:
                    self.decor.spawnDecor(
                        'ville_jour', x, -400, 1200, 1000, speed/5, 'x', False)
                else:
                    
                    self.decor.spawnDecor(
                        'ville_nuit', x, -200, 1200, 1000, speed/5, 'x', False)

            x += 1199
            for y in range(1, 5):
                self.decor.spawnDecor('tree1', treesx, randint(300, 400), randint(
                    150, 300), randint(500, 600), speed/2, 'x', False)
                treesx += randint(50, 150)

        # ground
        self.decor.spawnDecor('ground_1', 0, 600, 1024, 500, 0, 'x', True)
        

        x = 1024
        # obstacles
        for i in range(0, int(runLenght)):
            randy = randint(500, 600)
            randwidth = randint(50, 1000)
            self.decor.spawnDecor('ground_1', x, randy,
                                  randwidth, 1000, speed, 'x', True)

            if randint(0, 5) == 0:
                self.decor.spawnDecor(
                    'souche', x+randwidth/2, randy-100, 100, 150, speed, 'x', True)

            if randy >= 500:
                self.decor.spawnDecor(
                    'ground_1', x+randwidth, randint(650, 750), randint(50, 300), 1000, speed, 'x', True)

            x += randint(10, 1024)

            #stuff
            if randint(0,5) == 0: #salade
                self.decor.spawnIngredient(
                "Salade", x+randint(-100,100), 300, 50, 50, speed, "x", False)
            if randint(0,8) == 0: #pain
                self.decor.spawnIngredient(
                "Tomate", x+randint(-100,100), 300, 50, 50, speed, "x", False)
            if randint(0,10) == 0: #tomate
                self.decor.spawnIngredient(
                "Tomate", x+randint(-100,100), 300, 50, 50, speed, "x", False)
            if randint(0,20) == 0: #Comcombre
                self.decor.spawnIngredient(
                "Comcombre", x+randint(-100,100), 300, 50, 50, speed, "x", False)
            if randint(0,30) == 0: #Champignon
                self.decor.spawnIngredient(
                "Champignon", x+randint(-100,100), 300, 50, 50, speed, "x", False)
            if randint(0,30) == 0: #Patate
                self.decor.spawnIngredient(
                "Patate", x+randint(-100,100), 300, 50, 50, speed, "x", False)
            if randint(0,35) == 0: #Viande
                self.decor.spawnIngredient(
                "Viande", x+randint(-100,100), 300, 50, 50, speed, "x", False)
                

        self.decor.spawnDecor('house', x+100, 200, 600, 400, speed, 'x', False)
    def quitter(self):
        self.cacher()
        quit()

    def test(self):
        print("ok")

class Monster(pygame.sprite.Sprite):
    def __init__(self, coordinates, game):
        super().__init__()
        self.sound = Sound.Sound()
        self.game = game
        self.lastUpdatedFrame = time.time()
        self.updateJson()

        self.coordinates = coordinates
        self.hp = self.data['Monster']['hp']
        self.image = pygame.Surface([1, 1])
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates
        self.playerScale = (150, 275)

        self.collider = True

        self.sprites = []
        self.currentSprite = 0
        self.animationRate = 0.1

        self.speed_x = self.data['Monster']["speed_x"]
        self.speed_y = self.data['Monster']["speed_y"]
        self.gravity = self.data['Monster']["gravity"]
        self.jumpForce = self.data['Monster']["jumpForce"]

        self.animations = {}

        self.loadAnimations()

        self.isRunning = False

        self.isJumping = False
        self.isFlying = False

        self.playAnimation('groar', 1.5)


        self.jeu = game  # Creation instance jeu


    def loadAnimations(self):
        for i in self.data['Monster']['animations']:
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
            if type(sprite) is not Monster and sprite.collider and sprite.rect.colliderect((self.rect.x+39, self.rect.y+self.data['Monster']['height']-10, self.data['Player']['width']-10, 20)):

                return True
        return False

    def collisionY(self):
        for sprite in game.Game.get_instance().all_sprites:
            if type(sprite) is not Monster and sprite.collider and sprite.rect.colliderect((self.rect.x+39, self.rect.y+self.data['Monster']['height']-10, self.data['Player']['width']-10, 20)):
                self.speed_y = 0

    def collisionYdeep(self, nouvPos):
        for sprite in game.Game.get_instance().all_sprites:
            if type(sprite) is not Monster and sprite.collider and sprite.rect.colliderect((self.rect.x+37, self.rect.y+self.data['Monster']['height']-20, self.data['Player']['width']-8, 20)):
                self.speed_y = 0
                if self.isRiding:
                    nouvPos[1] -= 5
                else:
                    nouvPos[1] -= 1


    def collisionX(self, direction):
        for sprite in game.Game.get_instance().all_sprites:
            if direction == "left":
                if type(sprite) is not Monster and sprite.collider and sprite.rect.colliderect((self.rect.left+30, self.rect.y-20, self.data['Player']['width']/2, self.data['Player']['height'])):
                    return True
            else:
                if type(sprite) is not Monster and sprite.collider and sprite.rect.colliderect((self.rect.x+80, self.rect.y-20, self.data['Player']['width']/2, self.data['Player']['height'])):
                    return True
        return False

    def action(self,event):
        pass
        
    def update(self):
        if self.jeu.currentMenu == "gameMenu":

            self.currentSprite += self.animationRate

            nouvPos = list(self.coordinates)

            if self.jeu.isInRun:
            
                ############################## EN RUN ######################################


                if self.speed_y == 0:
                    
                                        
                    if not self.isJumping:
                        self.setAnimation('fastrun',0.9)

                    if self.currentSprite >= len(self.sprites):
                        self.currentSprite = 0               

                    if self.isJumping == True:
                        self.speed_y = self.jumpForce
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




                if not self.isOnGround() and not self.isJumping and not self.isFlying:   
                    self.isFlying = True      
                    self.speed_y = 0.1
                
                self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)
                self.collisionYdeep(nouvPos)
                self.collisionY()

                #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left, self.rect.y+20 ,self.data['Player']['width']/2,self.data['Player']['height']/2.5))
                #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+120, self.rect.y+20 ,self.data['Player']['width']/2,self.data['Player']['height']/2.5))
                #pygame.draw.rect(self.game.screen,(255,255,255),(self.rect.x+39 , self.rect.y+self.data['Player']['height'],self.data['Player']['width']-10,20))
                #pygame.draw.rect(self.game.screen,(0,0,255),(self.rect.x+80, self.rect.y-10 ,self.data['Player']['width']/2,self.data['Player']['height']))

            nouvPos[0] = 500
            self.coordinates = tuple(nouvPos)
            self.rect.topleft = self.coordinates     
   

    def updateJson(self):
        f = open('Data/config/config.json', "r")
        self.data = json.load(f)
        f.close()

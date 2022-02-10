from asyncore import loop
from random import randint
import pygame
import Bouton as bouton
from DecorElement import DecorElement
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
        # Ajout des boutons pour le me nu principal
        # self.text = fonction associe au bouton
        self.echapMenuButtons.add(
            bouton.Bouton(10, 10, "Reprendre", self.test))
        self.echapMenuButtons.add(bouton.Bouton(
            10, 100, "Retour menu", self.test))
        self.echapMenuButtons.add(bouton.Bouton(10, 300, "Quitter", self.test))

        self.lastClickedButton = None
        self.currentMenu = self.echapMenuButtons
        self.multiplicateurVitesseCamera = 1
        self.multiplicateurVitesseCameraDefinitif = 1

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
        self.nbJour = 1

        # Creation hud money / score / run
        self.moneyHUD = pygame.image.load(self.data['Items']['Money']['img']).convert_alpha()
        self.moneyHUD = pygame.transform.scale(self.moneyHUD, (70,60))
        self.moneyRect = self.moneyHUD.get_rect()
        self.moneyRect.topleft = (1000,10)
        self.fonts = pygame.font.Font(self.data["Font"]["base"], 36)
        self.txt = self.fonts.render(str(self.game.player.argent), True, (255,255,255))
        self.txtScore = self.fonts.render(str(self.game.player.score), True, (255,255,255))
        self.txtRun = self.fonts.render(str(self.game.nbRun), True, (255,255,255))

        self.speed = 0
        

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

    def generateWorld(self,nbRun,night):
        
        biome = 'ville'
        if (randint(0,1) == 1):
            biome = 'foret'
        
        if night:
            self.speed = (nbRun + 1)*self.multiplicateurVitesseCamera*self.multiplicateurVitesseCameraDefinitif *1.5
        else:
            self.speed = (nbRun + 1)*self.multiplicateurVitesseCamera*self.multiplicateurVitesseCameraDefinitif

        if nbRun >3:
            self.speed = self.speed/1.8

        runLenght = nbRun*1.5+10
        x = 0
        treesx = 0
        # fond
        if not night:
            self.music.playMusic(biome,"day", 0.09)
            self.decor.spawnDecor('sunset', 0, 0, self.data['Settings']['WIDTH'], self.data['Settings']['HEIGHT'], 0, 'x', False)
        else:
            self.music.playMusic(biome,"night", 0.09)
            self.decor.spawnDecor('moon', 0, 0, self.data['Settings']['WIDTH'], self.data['Settings']['HEIGHT'], 0, 'x', False)

        for i in range(0, int(runLenght)):
            if biome == 'foret':
                if not night:
                   
                    self.decor.spawnDecor(
                        'foret_jour', x, -200, 1200, 1000, self.speed/5, 'x', False)
                else:
                    
                    self.decor.spawnDecor(
                        'foret_nuit', x, -200, 1200, 1000, self.speed/5, 'x', False)
                   
            else :
                if not night:
                    self.decor.spawnDecor(
                        'ville_jour', x, -300, 1200, 1000, self.speed/5, 'x', False)
                else:
                    
                    self.decor.spawnDecor(
                        'ville_nuit', x, -290, 1200, 1000, self.speed/5, 'x', False)
                #grue 
                if randint(0, 30) == 0:
                    self.decor.spawnDecor('grue', treesx, 100, 652 , 500, self.speed/2, 'x', False)
            x += 1199

            #arbres
            for y in range(1, 5):
                if not night:
                    self.decor.spawnDecor('tree1', treesx, randint(300, 400), randint(
                        150, 300), randint(500, 600), self.speed/2, 'x', False)
                else:
                    self.decor.spawnDecor('tree1_n', treesx, randint(300, 400), randint(
                        150, 300), randint(500, 600), self.speed/2, 'x', False)
                treesx += randint(50, 150)

        groundsx = -100
        groundwidth = 2000
        for i in range(0, int(runLenght)):
            # ground
            self.decor.spawnDecor('ground_1', groundsx, 600, groundwidth, 500, self.speed, 'x', True,0,10)
            groundsx += groundwidth + 300
            groundwidth = randint(500,2000)
            

        x = 1024
        # obstacles
        for i in range(0, int(runLenght)):
            randy = randint(500, 600)
            randwidth = randint(50, 1000)
            self.decor.spawnDecor('ground_1', x, randy,
                                  randwidth, 500, self.speed, 'x', True,0,10)

            if randint(0, 5) == 0:
                self.decor.spawnDecor(
                    'souche', x+randwidth/2, randy-100, 100, 150, self.speed, 'x', True, 50, 10 ,20, 150)

            if randint(0, 10) == 0:
                self.decor.spawnDecor(
                    'ground_1',x+randwidth/5,  randy-100, randint(200, 300), 500, self.speed, 'x', True,0,10)
                self.decor.spawnDecor(
                    'bus', x+randwidth/2+100, randy-200, 500, 250, self.speed, 'x', True, 20,10)
                self.decor.spawnDecor(
                    'ground_1',x+randwidth/2+100,  randy+50, 500, 500, self.speed, 'x', True,0,10)

            if randint(0, 1) == 0:
                self.decor.spawnDecor(
                    'rocher', x+randwidth/2, randy, 250, 60, self.speed, 'x', True,0,10)

            if randy >= 500:
                self.decor.spawnDecor(
                    'ground_1', x+randwidth, randint(650, 750), randint(50, 300), 1000, self.speed, 'x', True,0,10)

            x += randint(10, 1024)

            #stuff
            if randint(0,self.data['Ingredients']['Salade']['rare']) == 0 or (night and randint(0,int(self.data['Ingredients']['Salade']['rare']*10)) == 0): #salade
                self.decor.spawnIngredient(
                "Salade", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)
            if randint(0,self.data['Ingredients']['Tomate']['rare']) == 0 or (night and randint(0,int(self.data['Ingredients']['Tomate']['rare']*10)) == 0): #pain
                self.decor.spawnIngredient(
                "Tomate", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)
            if randint(0,self.data['Ingredients']['Pain']['rare']) == 0 or (night and randint(0,int(self.data['Ingredients']['Pain']['rare']*10)) == 0): #tomate
                self.decor.spawnIngredient(
                "Pain", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)
            if randint(0,self.data['Ingredients']['Comcombre']['rare']) == 0 or (night and randint(0,int(self.data['Ingredients']['Comcombre']['rare']*10)) == 0): #Comcombre
                self.decor.spawnIngredient(
                "Comcombre", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)
            if randint(0,self.data['Ingredients']['Champignon']['rare']) == 0 or (night and randint(0,int(self.data['Ingredients']['Champignon']['rare']*10)) == 0): #Champignon
                self.decor.spawnIngredient(
                "Champignon", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)
            if randint(0,self.data['Ingredients']['Patate']['rare']) == 0 or (night and randint(0,int(self.data['Ingredients']['Patate']['rare']*10)) == 0): #Patate
                self.decor.spawnIngredient(
                "Patate", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)
            if randint(0,self.data['Ingredients']['Viande']['rare']) == 0 or (night and randint(0,int(self.data['Ingredients']['Viande']['rare']*10)) == 0): #Viande
                self.decor.spawnIngredient(
                "Viande", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)
            if randint(0,self.data['Ingredients']['Sucre']['rare']*10) == 0 or (night and randint(0,int(self.data['Ingredients']['Sucre']['rare']/1.5)) == 0): #Sucre
                self.decor.spawnIngredient(
                "Sucre", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)
            if randint(0,self.data['Ingredients']['Saumon']['rare']*10) == 0 or (night and randint(0,int(self.data['Ingredients']['Saumon']['rare']/1.5)) == 0): #Saumon
                self.decor.spawnIngredient(
                "Saumon", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)
            if randint(0,self.data['Ingredients']['Caviar']['rare']*10) == 0 or (night and randint(0,int(self.data['Ingredients']['Caviar']['rare']/1.5)) == 0): #Caviar
                self.decor.spawnIngredient(
                "Caviar", x+randint(-1000,1000), 300, 50, 50, self.speed, "x", False)

            #dollars
            if randint(0,5) == 0:
                dx = x
                for posd in range(0,5):
                    self.decor.spawnDecor(
                        'money', dx, randint(400,500), 50, 60, self.speed, 'x', False)
                    dx += 100

                

        self.decor.spawnDecor('house', x+100, -200, 600, 900, self.speed, 'x', False,200,0)


    def updateMoney(self,screen):

        screen.blit(self.moneyHUD, (10,2))
        self.txt = self.fonts.render(str(self.game.player.argent), True, (255,255,255))
        self.txtScore = self.fonts.render("Score "+str(self.game.player.score), True, (255,255,255))
        if self.game.night:
            self.txtRun = self.fonts.render("Run " + str(self.game.nbRun), True, (255,0,0))
        else:
            self.txtRun = self.fonts.render("Run " + str(self.game.nbRun), True, (255,255,255))
        screen.blit(self.txt, (80,10))
        screen.blit(self.txtScore, (10,60))
        screen.blit(self.txtRun, (10,110))
        


        
        
        

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
        self.lastSoundPlay = time.time()
        self.updateJson()

        self.coordinates = coordinates
        self.hp = self.data['Monster']['hp']
        self.image = pygame.Surface([1, 1])
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates
        self.playerScale = (300, 500)

        self.collider = True

        self.multiplicateurVitesseCamera = 1
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

        self.isStarting = False


        self.jeu = game  # Creation instance jeu

        self.cacher()

        self.speed = 0

    def afficher(self):
        self.image.set_alpha(255)
        self.isStarting = True
        self.playAnimation('groar', 0.8)

    def cacher(self):
        self.image.set_alpha(0)

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
            if type(sprite) is not Monster and sprite.collider and sprite.rect.colliderect((self.rect.x+39, self.rect.y+360, 150, 20)):

                return True
        return False

    def collisionY(self):
        for sprite in game.Game.get_instance().all_sprites:
            if type(sprite) is not Monster and sprite.collider and sprite.rect.colliderect((self.rect.x+39, self.rect.y+360, 150, 20)):
                self.speed_y = 0

    def collisionYdeep(self, nouvPos):
        for sprite in game.Game.get_instance().all_sprites:
            if type(sprite) is not Monster and sprite.collider and sprite.rect.colliderect((self.rect.x+39, self.rect.y+350, 150, 20)):
                self.speed_y = 0
                nouvPos[1] -= 5



    def collisionX(self):
        for sprite in game.Game.get_instance().all_sprites:
                if type(sprite) is not Monster and sprite.collider and sprite.rect.colliderect((self.rect.x+130, self.rect.y+180, 50, 150)):
                    return True
        return False

    def collisionPlayer(self):
        for sprite in game.Game.get_instance().characters:
                if type(sprite) is not Monster and sprite.rect.colliderect((self.rect.x+130, self.rect.y+180, 50, 150)):
                    return True
        return False

    def action(self,event):
        pass
        
    def update(self):
        if self.jeu.currentMenu == "gameMenu":
            
            self.currentSprite += self.animationRate

            nouvPos = list(self.coordinates)

            if self.jeu.isInRun and self.jeu.night:          
                if (time.time() >= self.lastSoundPlay + 18): 
                    self.lastSoundPlay = time.time()
                    self.sound.MonsterGroar(.06)
                ############################## EN RUN ######################################
                if not self.isStarting:
                    if self.collisionX():
                        self.isJumping = True

                    if self.speed_y == 0:
                        
                        self.isFlying = False
                                            
                        if not self.isJumping:
                            self.setAnimation('run',0.9)              

                        if self.isJumping == True:
                            self.speed_y = self.jumpForce
                            nouvPos[1] -= self.speed_y
                            self.playAnimation('jumploop',3)
                            

                    elif self.speed_y != 0:

                        if self.isJumping == True:
                            
                            nouvPos[1]-= self.speed_y #(-0.001*(y[0]*y[0]))
                            if self.speed_y > 0.5:
                                self.speed_y -= 0.5
                                
                            else:
                                self.speed_y = 0.1
                                self.isJumping = False             

                        else:
                            
                            self.setAnimation('jumploop',3)
                            self.speed_y +=0.2
                            nouvPos[1] += self.speed_y

                            if self.speed_y >= 10:
                                self.isFallingHard = True
                            if self.speed_y <= 1.5:
                                self.isFallingSlow = True


                if self.currentSprite >= len(self.sprites):
                    if self.isStarting:
                        self.isStarting = False
                    self.currentSprite = 0 

                if not self.isOnGround() and not self.isJumping and not self.isFlying:   
                    self.isFlying = True      
                    self.speed_y = 0.1
                
                self.image = pygame.transform.flip(self.sprites[int(self.currentSprite)], True, False)
                self.collisionYdeep(nouvPos)
                self.collisionY()

                #pygame.draw.rect(self.game.screen,(0,0,255),(self.rect.x+80, self.rect.y-10 ,self.data['Player']['width']/2,self.data['Player']['height']))

                if self.isStarting:
                     nouvPos[1] = 250

                nouvPos[0] = -40
                self.coordinates = tuple(nouvPos)
                self.rect.topleft = self.coordinates   

                if self.collisionPlayer():
                    self.game.player.GameOver()
            else:
                self.cacher()
                self.sound.StopGroar()

            
                    
            

    def updateJson(self):
        f = open('Data/config/config.json', "r")
        self.data = json.load(f)
        f.close()

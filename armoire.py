from re import X
import pygame
import json
from random import randint
import InventoryItem
from Sound import Sound
class armoire(pygame.sprite.Sprite):
    def __init__(self, game, planque):
        pygame.sprite.Sprite.__init__(self)
        file = open('Data/config/config.json', "r")
        self.data = json.load(file)
        file.close()

        self.planque = planque
        self.game = game
        self.collider = False
        self.isVisible = False

        self.backgroundArmoire = pygame.image.load(
            self.data["Background_images"]["armoire"]).convert_alpha()
        self.image = self.backgroundArmoire
        self.image = pygame.transform.scale(self.image,(800,800))

        self.rect = self.image.get_rect()
        self.rect.topleft = (100,10)  

        # Chargement sprite ingredients
        self.ingredientsImg = {}

        self.ingredientsGroup = pygame.sprite.Group()
        for ingredient in self.data["Ingredients"]:
            self.ingredientsImg[ingredient] = pygame.image.load(
                self.data["Ingredients"][ingredient]["img"]).convert_alpha()

        # Chargement sprite plats
        self.platsImg = {}
        for plat in self.game.playground.plats:
            self.platsImg[plat] = self.game.playground.plats[plat]['img']
        print(self.platsImg)


    def afficher(self):  
        
        self.updateAfficher()
        
        self.game.all_sprites.add(self)
        
        self.game.all_sprites.add(self.ingredientsGroup)
        self.isVisible = True
        self.planque.isInMenu = True

    def updateAfficher(self):
        
        x = 200
        y = 90
        y_offset = y
        for ingredient in self.game.player.inventory['Ingredients']:
            if self.game.player.inventory['Ingredients'][ingredient] > 0:
                for i in range(0,self.game.player.inventory['Ingredients'][ingredient]):
                    self.ingredientsGroup.add(ArmoireButton(
                        ingredient, self.game.player.inventory['Ingredients'][ingredient], self.ingredientsImg[ingredient], x, y,  self.data["Ingredients"][ingredient]["width"],  self.data["Ingredients"][ingredient]["height"], self, 'ingredient'))
                    x+=30
                    y = randint(y_offset-5,y_offset+5)

                x = 200
                y_offset += 60
                y = y_offset
        
        for plats in self.game.player.inventory['Plats']:
            if len(self.game.player.inventory['Plats'][plats]) > 0:
                for i in self.game.player.inventory['Plats'][plats]:
                    
                    self.ingredientsGroup.add(ArmoireButton(
                        i.name, self.game.player.inventory['Plats'][plats], self.platsImg[plats], x, y,  self.data["Plats"][plats]["width"],  self.data["Plats"][plats]["height"], self, 'plat',i))
                    x+=50
                    y = randint(y_offset-5,y_offset+5)

                x = 200
                y_offset += 60
                y = y_offset

    def cacher(self):
        
        self.game.all_sprites.remove(self)
        self.game.all_sprites.remove(self.ingredientsGroup)
        self.ingredientsGroup.empty()
        
        self.isVisible = False
        self.planque.isInMenu = False

    def isOverred(self):  
        mouse = pygame.mouse.get_pos()
        if self.rect.colliderect((mouse[0], mouse[1], 5, 5)) and self.isVisible:
            return True
        else:
            return False

    def isQuitting(self):
        if not self.isOverred() and pygame.mouse.get_pressed()[0] and self.isVisible:
            return True
        else:
            return False

    def update(self):
        if self.isQuitting():
            self.cacher()


class ArmoireButton(pygame.sprite.Sprite):
    def __init__(self, nom, nombre, img, x, y, width, height, armoire, type,obj = None):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.nom = nom
        self.obj = obj
        self.nombre = nombre
        self.image = img
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.armoire = armoire
        self.collider = False
        
        self.sound = self.armoire.game.sons
 
        self.statsHUD = pygame.image.load(self.armoire.data['Items']['Stats_planche']['img']).convert_alpha()
        self.fonts = pygame.font.Font(self.armoire.data["Font"]["base"], 36)


    def isClicked(self):  # Si la souris clique sur le bouton
        mouse = pygame.mouse.get_pos()
        if self.isOverred() and pygame.mouse.get_pressed()[0] and self.armoire.isVisible:
            return True
        else:
            return False

    def isOverred(self):  # Si la souris passe sur le bouton
        mouse = pygame.mouse.get_pos()
        if self.rect.colliderect((mouse[0], mouse[1], 5, 5)) and self.armoire.isVisible:
            return True
        else:
            return False

    def afficherStats(self,screen):

        
        if self.obj.type == "speed":     
            self.statsHUD = pygame.transform.scale(self.statsHUD, (200,60))   
            screen.blit(self.statsHUD, (self.rect.x +10 ,self.rect.y -45))
            txt = self.fonts.render("Vitesse : +"+str(round(self.obj.stats*100,2))+"%", True, (255,255,255))
            screen.blit(txt, (self.rect.x +10+5 ,self.rect.y -40))
        elif self.obj.type == "saut":
            self.statsHUD = pygame.transform.scale(self.statsHUD, (200,60))   
            screen.blit(self.statsHUD, (self.rect.x +10 ,self.rect.y -45))
            txt = self.fonts.render("Saut : +"+str(round(self.obj.stats*100,2))+"%", True, (255,255,255))
            screen.blit(txt, (self.rect.x +10+5 ,self.rect.y -40))
        elif self.obj.type == "ralentissement":
            self.statsHUD = pygame.transform.scale(self.statsHUD, (300,60))   
            screen.blit(self.statsHUD, (self.rect.x +10 ,self.rect.y -45))
            txt = self.fonts.render("Ralentissement : -"+str(round(self.obj.stats*100,2))+"%", True, (255,255,255))
            screen.blit(txt, (self.rect.x +10+5 ,self.rect.y -40))

        
        
        

    def update(self):

        if self.isClicked():
            self.sound.playSound("eating",0.5)
            print (self.nom)
            if self.obj is None:
                self.armoire.game.player.inventory['Ingredients'][self.nom] -= 1
                bonus = self.armoire.game.player.data["Ingredients"][self.nom]["bonus"]
                if bonus["type"] == "speed":
                    self.armoire.game.player.multiplicateurVitesse += bonus["value"]
                    print("Vitesse : " + str(self.armoire.game.player.multiplicateurVitesse))

                elif bonus["type"] == "saut":
                    self.armoire.game.player.multiplicateurSaut += bonus["value"]
                    print("Saut : " + str(self.armoire.game.player.multiplicateurSaut))
                elif bonus["type"] == "ralentissement":
                    if(self.armoire.game.playground.multiplicateurVitesseCamera - bonus["value"] > 0.05):
                        self.armoire.game.playground.multiplicateurVitesseCamera -= bonus["value"]
                    print("VitesseCamera : " + str(self.armoire.game.playground.multiplicateurVitesseCamera))

                ###### A COMPLETER : apllique les effets ####

            else:
                if self.obj.type == "speed":
                    self.armoire.game.player.multiplicateurVitesse+= self.obj.stats

                elif self.obj.type == "saut":
                    self.armoire.game.player.multiplicateurSaut += self.obj.stats
                elif self.obj.type == "ralentissement":
                    if(self.armoire.game.playground.multiplicateurVitesseCamera - self.obj.stats > 0.05):
                        self.armoire.game.playground.multiplicateurVitesseCamera -= self.obj.stats
                self.armoire.game.player.inventory['Plats'][self.nom].remove(self.obj) 

            self.armoire.updateAfficher()
            self.kill()

        if self.isOverred():
            if self.obj != None:
                self.afficherStats(self.armoire.game.screen)

                
            
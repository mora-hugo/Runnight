from re import X
import pygame
import json
from random import randint


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
        self.image = pygame.transform.scale(self.image,(700,700))

        self.rect = self.image.get_rect()
        self.rect.topleft = (150,50)  

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
        x = 250
        y = 120
        y_offset = y
        for ingredient in self.game.player.inventory['Ingredients']:

            for i in range(0,self.game.player.inventory['Ingredients'][ingredient]):
                self.ingredientsGroup.add(ArmoireButton(
                    ingredient, self.game.player.inventory['Ingredients'][ingredient], self.ingredientsImg[ingredient], x, y,  self.data["Ingredients"][ingredient]["width"],  self.data["Ingredients"][ingredient]["height"], self, 'ingredient'))
                x+=15
                y = randint(y_offset-5,y_offset+5)

            x = 250
            y_offset += 60
            y = y_offset
        
        for plats in self.game.player.inventory['Plats']:

            for i in range(0,self.game.player.inventory['Plats'][plats]):
                self.ingredientsGroup.add(ArmoireButton(
                    plats, self.game.player.inventory['Plats'][plats], self.platsImg[plats], x, y,  self.data["Plats"][plats]["width"],  self.data["Plats"][plats]["height"], self, 'plat'))
                x+=15
                y = randint(y_offset-5,y_offset+5)

            x = 250
            y_offset += 60
            y = y_offset

    def cacher(self):
        self.game.all_sprites.remove(self)
        self.game.all_sprites.remove(self.ingredientsGroup)
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
    def __init__(self, nom, nombre, img, x, y, width, height, armoire, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.nom = nom
        self.nombre = nombre
        self.image = img
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.armoire = armoire
        self.collider = False


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

    def update(self):

        if self.isClicked():
            print (self.nom)
            if self.type == 'ingredient':
                self.armoire.game.player.inventory['Ingredients'][self.nom] -= 1

                ###### A COMPLETER : apllique les effets ####

            else:
                self.armoire.game.player.inventory['Plats'][self.nom] -= 1

                ###### A COMPLETER : apllique les effets ####
                
            self.armoire.updateAfficher()
            self.kill()
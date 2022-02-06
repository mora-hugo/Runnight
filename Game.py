from html import entities
import pygame
import Menu
import json
import Player

class Game(): #Design pattern singleton
    instance = None
    @classmethod
    def get_instance(self):
        if Game.instance is None :
            Game.instance = Game()

        return Game.instance

    def __init__(self):
        if Game.instance is not None:
            raise Exception("Utiliser la méthode get_instance() pour obtenir une instance de l'objet")
        else:
            pygame.init()
            pygame.display.set_caption("WATIBJEU") # Nom de la fenetre
            self.screen = pygame.display.set_mode((1024,768)) # taille + mode , ...
            self.all_sprites = pygame.sprite.Group() # Variables ou tous les sprites seront stockés
            self.menu = Menu.Menu() # Creer menu
            self.background_image = pygame.image.load("Data/sprites/background.jpg").convert() #Chargement background
            self.screen.blit(self.background_image,(0,0))

            #Toutes les touches pressés par le joueur
            self.key_pressed = {}

            #config file load
            f = open('Data/config/config.json')
            self.data = json.load(f)
            self.isMapping = False

            self.load_keys()

            #Joueur
            self.player = Player.Player((400,-100),self)
            self.all_sprites.add(self.player)

    def load_keys(self):
        for i in self.data['Bindings']:
            self.key_pressed[self.data['Bindings'][i]] = False

    def update_background(self):
        self.screen.blit(self.background_image,(0,0))

    def get_keys(self,event):
        if event.type == pygame.KEYDOWN:
            self.key_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            self.key_pressed[event.key] = False

    def mapping(self):

        key_pressed = self.menu.data["Bindings"][self.menu.lastClickedButton.touche]
        for key in self.key_pressed:
            if self.key_pressed[key] == True:
                key_pressed = key
                self.menu.lastClickedButton.updateKey(self.menu.lastClickedButton.touche,key)
                self.menu.data["Bindings"][self.menu.lastClickedButton.touche] = key_pressed
                file = open('Data/config/config.json',"w")
                self.isMapping = False
                json.dump(self.menu.data,file,indent=4)
                file.close()
                self.player.updateJson()

    def update(self):
        print(self.key_pressed)
        if self.isMapping == True:
            self.mapping()
        self.update_background()
        self.all_sprites.draw(self.screen)
        self.all_sprites.update()
        pygame.display.flip()

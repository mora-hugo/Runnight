from html import entities
import pygame
import Menu
import json
import Player
import Playground
import Chargement
import Decor
import Sound
import Planque


class Game():  # Design pattern singleton
    instance = None

    @classmethod
    def get_instance(self):
        if Game.instance is None:
            Game.instance = Game()

        return Game.instance

    def __init__(self):
        if Game.instance is not None:
            raise Exception(
                "Utiliser la méthode get_instance() pour obtenir une instance de l'objet")
        else:
            pygame.init()
            pygame.display.set_caption("WATIBJEU")  # Nom de la fenetre
            # taille + mode , ...
            self.screen = pygame.display.set_mode((1024, 768))

            # Variables ou tous les sprites seront stockés
            self.all_sprites = pygame.sprite.Group()
            self.barre = Chargement.Chargement(self.screen, "Chargement menu")
            self.menu = Menu.Menu(self)  # Creer menu
            self.barre.update(20, "Chargement de l'environnement de jeu")

            self.screen.blit(self.menu.background_image, (0, 0))

            # Toutes les touches pressés par le joueur
            self.key_pressed = {}

            # config file load
            f = open('Data/config/config.json')
            self.data = json.load(f)
            self.isMapping = False

            self.load_keys()

            # Joueur
            self.barre.update(60, "Chargement joueur")
            self.player = Player.Player((400, 200), self)
            self.all_sprites.add(self.player)

            self.currentMenu = "mainMenu"

            # Sons

            self.barre.update(65, "Chargement Sons")
            self.sons = Sound.Sound()
            # Decor
            self.barre.update(80, "Chargement décors")
            self.decor = Decor.Decor(self)

            self.playground = Playground.Playground(self.screen, self)

            # Planque
            self.barre.update(90, "Chargmement de la planque")
            self.planque = Planque.Planque(self)

    def load_keys(self):
        for i in self.data['Bindings']:
            self.key_pressed[self.data['Bindings'][i]] = False

    def get_keys(self, event):
        if event.type == pygame.KEYDOWN:
            self.key_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            self.key_pressed[event.key] = False

    def mapping(self):

        key_pressed = self.menu.data["Bindings"][self.menu.lastClickedButton.touche]
        for key in self.key_pressed:
            if self.key_pressed[key] == True:
                key_pressed = key
                self.menu.lastClickedButton.updateKey(
                    self.menu.lastClickedButton.touche, key)
                self.menu.data["Bindings"][self.menu.lastClickedButton.touche] = key_pressed
                file = open('Data/config/config.json', "w")
                self.isMapping = False
                json.dump(self.menu.data, file, indent=4)
                file.close()
                self.player.updateJson()

    def startRun(self, biome, night):
        self.playground.generateWorld(biome, night)

    def update_backgrounds(self):
        if self.currentMenu == "mainMenu":
            self.menu.update_background()
        elif self.currentMenu == "gameMenu":
            self.playground.update_background()

    def update(self):
        if self.isMapping == True:
            self.mapping()
        self.update_backgrounds()
        self.all_sprites.draw(self.screen)

        self.all_sprites.update()
        pygame.display.flip()

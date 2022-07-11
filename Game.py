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
import Bibliotheque

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
            pygame.display.set_caption("RUN'NIGHT") # Nom de la fenetre
            self.screen = pygame.display.set_mode((1024,768)) # taille + mode , ...
            
            self.nbRun = 1

            self.isInRun = False

            self.night = False

            self.all_sprites = pygame.sprite.Group() # Variables ou tous les sprites seront stockés
            self.characters = pygame.sprite.Group()
            self.barre = Chargement.Chargement(self.screen,"Chargement menu")
            self.menu = Menu.Menu(self) # Creer menu
            self.barre.update(20,"Chargement de l'environnement de jeu")
            
            
            self.screen.blit(self.menu.background_image,(0,0))

            #Toutes les touches pressés par le joueur
            self.key_pressed = {}

            #Souris touche par le joueur
            self.mouse_pressed = -1 # -1 = rien, 0 mouse down, 1 mouse up  

            # config file load
            f = open('Data/config/config.json')
            self.data = json.load(f)
            self.isMapping = False

            self.load_keys()

            #Joueur
            self.barre.update(40,"Chargement joueur")
            self.player = Player.Player((400,200),self)
            self.characters.add(self.player)
            
            self.currentMenu = "mainMenu"

            # Sons

            self.barre.update(60, "Chargement Sons")
            self.sons = Sound.Sound()
            # Decor
            self.barre.update(70, "Chargement décors")
            self.decor = Decor.Decor(self)

            self.playground = Playground.Playground(self.screen, self)

            # Planque
            self.barre.update(80, "Chargement de la planque")
            self.planque = Planque.Planque(self)

            # Monstre
            self.barre.update(90, "Chargement des entites")
            self.monster = Playground.Monster((0,200),self)
            self.characters.add(self.monster)

            
    def load_keys(self):
        for i in self.data['Bindings']:
            self.key_pressed[self.data['Bindings'][i]] = False

    def get_keys(self, event):
        if event.type == pygame.KEYDOWN:
            self.key_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            self.key_pressed[event.key] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pressed = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_pressed = 1
        else:
            self.mouse_pressed = -1

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

    def startRun(self):
        self.isInRun = True
        self.player.tpRun = True
        self.planque.cacher()
        if self.night:
            self.monster.afficher()
        self.playground.generateWorld(self.nbRun,self.night)
        pause = False

#Main loop
        

    def update_backgrounds(self):
        if self.currentMenu == "mainMenu":
            #mise a zero des valeurs lorsque dans le menu
            self.nbRun = 1

            self.isInRun = False

            self.night = False
            self.player.inventory = {"Ingredients" : {},"Plats" : {}}

            self.player.multiplicateurVitesseDefinitif = 1
            self.player.multiplicateurSautDefinitif = 1
            self.player.multiplicateurVitesse = 1
            self.player.multiplicateurSaut = 1
            self.player.isRunning = False
            self.player.speed_y = 0
            self.player.argent = 0
            self.player.score = 0

            self.playground.multiplicateurVitesseCamera = 1
            self.playground.multiplicateurVitesseCameraDefinitif = 1

            self.player.bonusRiding = 0
            self.player.hardLandingBonus = 0
            self.menu.afficher()
            self.planque.cacher()
            self.monster.cacher()
        elif self.currentMenu == "gameMenu":
            self.playground.update_background()

    def update(self):
        if self.isMapping == True:
            self.mapping()
        self.update_backgrounds()
        self.all_sprites.draw(self.screen)
        self.characters.draw(self.screen)
        self.all_sprites.update()
        self.characters.update()
        if self.currentMenu == "gameMenu":
            self.playground.updateMoney(self.screen)
        pygame.display.flip()

import pygame
import Model.Menu
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
            self.menu = Model.Menu.Menu() # Creer menu
            self.background_image = pygame.image.load("Data/sprites/background.jpg").convert() #Chargement background
            self.screen.blit(self.background_image,(0,0))
    def update_background(self):
        self.screen.blit(self.background_image,(0,0))

import pygame
import Bouton as bouton
import Game as game
import json


class Playground:
    def __init__(self, screen):
        # Tableaux contenant tous les boutons du menu
        self.echapMenuButtons = pygame.sprite.Group()


        #Ajout des boutons pour le menu principal
        self.echapMenuButtons.add(bouton.Bouton(10,10,"Reprendre",self.test)) #self.text = fonction associe au bouton
        self.echapMenuButtons.add(bouton.Bouton(10,100,"Retour menu",self.test))
        self.echapMenuButtons.add(bouton.Bouton(10,300,"Quitter",self.test))

        self.lastClickedButton = None
        self.currentMenu = self.echapMenuButtons

        #Lecture du json pour les data
        file = open('Data/config/config.json',"r")
        self.data = json.load(file)
        file.close()

        #Background de bg
        self.background_image = pygame.image.load(self.data["Background_images"]["gameMenu"]).convert() #Chargement background

        self.ground = pygame.Rect(0,550,1024,500)
        pygame.draw.rect(screen,(255,255,255),self.ground)
        



    #Affiche les elements du menu
    def afficher(self,group_menu = None):
        if group_menu == None: # si pas de menu rentré, alors mettre le menu de base
            group_menu = self.echapMenuButtons
        jeu = game.Game.get_instance()
        jeu.all_sprites.add(group_menu)

    #Cache les elements du menu
    def cacher(self,group_menu = None):
        if group_menu == None: # si pas de menu rentré, alors mettre le menu de base
            group_menu = self.echapMenuButtons
        jeu = game.Game.get_instance()
        jeu.all_sprites.remove(group_menu)
        self.update_background()
    #Switch to gameMenu
    def gameMenu(self):
        self.cacher(self.currentMenu)
        self.afficher(self.echapMenuButtons)
        self.currentMenu = self.echapMenuButtons

    def goToGame(self):
        self.cacher(self.currentMenu)
        self.currentMenu = None

    def update_background(self):
        game.Game.get_instance().screen.blit(self.background_image,(0,0))

    def quitter(self):
        self.cacher()
        quit()

    def test(self):
        print("ok")

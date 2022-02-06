import pygame
import Bouton as bouton
import BoutonTouche as boutonT
import Game as game
import json




class Menu:
    def __init__(self):
        # Tableaux contenant tous les boutons du menu
        self.mainMenuButtons = pygame.sprite.Group()
        # Tableaux contenant tous les boutons des binds
        self.menuBidingButtons = pygame.sprite.Group()


        #Ajout des boutons pour le menu principal
        self.mainMenuButtons.add(bouton.Bouton(10,10,"Commencer",self.commencer)) #self.text = fonction associe au bouton
        self.mainMenuButtons.add(bouton.Bouton(10,100,"Règle",self.regles))
        self.mainMenuButtons.add(bouton.Bouton(10,200,"Touches",self.menuTouches))
        self.mainMenuButtons.add(bouton.Bouton(10,300,"Quitter",self.quitter))

        self.lastClickedButton = None
        self.currentMenu = self.mainMenuButtons
        #ouverture fichier config
        file = open('Data/config/config.json',"r")
        self.data = json.load(file)
        file.close()
        #Ajout des boutons pour les bindings
        offset = 10
        for nom in self.data["Bindings"]:
            btn = boutonT.BoutonTouche(300,offset,nom,self.data["Bindings"][nom],self.changerTouches)
            self.menuBidingButtons.add(btn) #self.text = fonction associe au bouton
            offset += 100
        self.menuBidingButtons.add(bouton.Bouton(10,offset,"Retour",self.mainMenu))
    #Affiche les elements du menu
    def afficher(self,group_menu = None):
        if group_menu == None: # si pas de menu rentré, alors mettre le menu de base
            group_menu = self.mainMenuButtons
        jeu = game.Game.get_instance()
        jeu.all_sprites.add(group_menu)

    #Cache les elements du menu
    def cacher(self,group_menu = None):
        if group_menu == None: # si pas de menu rentré, alors mettre le menu de base
            group_menu = self.mainMenuButtons
        jeu = game.Game.get_instance()
        jeu.all_sprites.remove(group_menu)
        jeu.update_background()
    def mainMenu(self):
        self.cacher(self.currentMenu)
        self.afficher(self.mainMenuButtons)
        self.currentMenu = self.mainMenuButtons
    def menuTouches(self):
        self.cacher(self.currentMenu)
        self.afficher(self.menuBidingButtons)
        self.currentMenu = self.menuBidingButtons

    def changerTouches(self):
        jeu = game.Game.get_instance()
        if jeu.isMapping == False:
            self.lastClickedButton.updateText(self.lastClickedButton.touche + " : ...") #Pour montrer que le changement est en cours
            jeu.isMapping = True




    def quitter(self):
        self.cacher()
        quit()
    def regles(self):
        print("Voici les regles")
    def commencer(self):
        print("commencer")

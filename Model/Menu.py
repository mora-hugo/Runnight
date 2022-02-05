import pygame
import Model.Bouton as bouton
import Model.Game as game


class Menu:
    def __init__(self):

        self.buttons = [] # Tableaux contenant tous les boutons du menu

        #Ajout des boutons
        self.buttons.append(bouton.Bouton(10,10,"Commencer",self.commencer)) #self.text = fonction associe au bouton
        self.buttons.append(bouton.Bouton(10,100,"Règle",self.regles))
        self.buttons.append(bouton.Bouton(10,200,"Quitter",self.quitter))

    #Affiche les elements du menu
    def afficher(self):
        jeu = game.Game.get_instance()
        for btn in self.buttons:
            jeu.all_sprites.add(btn)

    #Cache les elements du menu
    def cacher(self):
        jeu = game.Game.get_instance()
        for btn in self.buttons:
            jeu.all_sprites.remove(btn)
        jeu.update_background()

    def quitter(self):
        self.cacher()
    def regles(self):
        print("Voici les regles")
    def commencer(self):
        print("commencer")

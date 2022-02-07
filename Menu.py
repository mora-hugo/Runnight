import pygame
import Bouton as boutonN
import BoutonMenu as bouton
import BoutonTouche as boutonT
import Game as game
import json
import Classement
import Parchemin




class Menu:
    def __init__(self,jeu):
        # Tableaux contenant tous les boutons du menu
        self.mainMenuButtons = pygame.sprite.Group()
        # Tableaux contenant tous les boutons des binds
        self.menuBidingButtons = pygame.sprite.Group()


        #Ajout des boutons pour le menu principal
        self.mainMenuButtons.add(bouton.BoutonMenu(720,430 ,"Commencer",self.commencer,-5)) #self.text = fonction associe au bouton
        self.mainMenuButtons.add(bouton.BoutonMenu(250,480,"Regles",self.regles,-5))
        self.mainMenuButtons.add(bouton.BoutonMenu(465,410,"Touches",self.menuTouches,5))
        self.mainMenuButtons.add(bouton.BoutonMenu(10,440,"Quitter",self.quitter,-5))

        self.lastClickedButton = None
        self.currentMenu = self.mainMenuButtons
        #ouverture fichier config
        file = open('Data/config/config.json',"r")
        self.data = json.load(file)
        file.close()
        #Ajout des boutons pour les bindings
        self.menuBidingButtons.add(Parchemin.Parchemin(self))
        offset = 70
        for nom in self.data["Bindings"]:
            btn = boutonT.BoutonTouche(350,offset,nom,self.data["Bindings"][nom],self.changerTouches)
            self.menuBidingButtons.add(btn) #self.text = fonction associe au bouton
            offset += 70
        self.menuBidingButtons.add(boutonN.Bouton(350,offset,"Retour",self.mainMenu,(0,0,0)))

        #Background de bg
        self.background_image = pygame.image.load(self.data["Background_images"]["mainMenu"]).convert() #Chargement background
        jeu.barre.update(10,"Connexion...")
        classement = Classement.Classement(jeu)
        classement.initSprites()
        self.mainMenuButtons.add(classement.getScores())
        
        #Load le parchemin
        self.papier = pygame.image.load(self.data["Items"]["papier"]['img']).convert_alpha()

        self.papier = pygame.transform.scale(self.papier,(self.data["Items"]["papier"]["WIDTH"]*1.8,self.data["Items"]["papier"]["HEIGHT"]*1.8))

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
        self.update_background()

    def mainMenu(self):
        self.cacher(self.currentMenu)
        
        self.afficher(self.mainMenuButtons)
        self.currentMenu = self.mainMenuButtons
        self.update_background()

    def menuTouches(self):
        
        self.cacher(self.currentMenu)
        game.Game.get_instance().screen.blit(self.papier,(self.data["Settings"]["WIDTH"]/2 - self.data["Items"]["papier"]["WIDTH"]/2*1.8 ,self.data["Settings"]["HEIGHT"]/2 -self.data["Items"]["papier"]["HEIGHT"]/2*1.8))
        self.afficher(self.menuBidingButtons)
        self.currentMenu = self.menuBidingButtons
        

    def changerTouches(self):
        jeu = game.Game.get_instance()
        if jeu.isMapping == False:
            self.lastClickedButton.updateText(self.lastClickedButton.touche + " : ...") #Pour montrer que le changement est en cours
            jeu.isMapping = True

    def update_background(self):
        game.Game.get_instance().screen.blit(self.background_image,(0,0))

    def quitter(self):
        self.cacher()
        quit()
    def regles(self):
        print("Voici les regles")
    def commencer(self):
        self.cacher()
        self.startGame()

    def startGame(self):
        jeu = game.Game.get_instance()
        jeu.playground.update_background()
        jeu.currentMenu = "gameMenu"
        jeu.startRun('forest',False)

from random import randint
import pygame
import Bouton as bouton
import Game as game
import json


class Playground:
    def __init__(self, screen, game):
        self.game = game
        self.decor = game.decor

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


    def generateWorld(self,biome,night,nbRun):
        speed = nbRun + 1
        runLenght = nbRun*1.5+20
        x = 0
        treesx = 0
        #fond
        for i in range(0,int(runLenght)):
            if biome == 'foret':
                if not night:
                        self.decor.spawnDecor('foret_jour',x,-200,1200,1000,speed/5,'x',False)             
                else:
                        self.decor.spawnDecor('foret_nuit',x,-200,1200,1000,speed/5,'x',False)
            x += 1199
            for y in range(1,5):
                    self.decor.spawnDecor('tree1',treesx,randint(300,400),randint(150,300),randint(500,600),speed/2,'x',False)
                    treesx += randint(50,150)

        #ground
        self.decor.spawnDecor('ground_1',0,600,1024,500,0,'x',True)


        x = 1024      
        #obstacles
        for i in range(0,int(runLenght)):
            randy = randint(500,600)
            randwidth = randint(50,1000)
            self.decor.spawnDecor('ground_1',x,randy,randwidth,1000,speed,'x',True)

            if randint(0,5) == 0:
                self.decor.spawnDecor('souche',x+randwidth/2,randy-100,100,150,speed,'x',True)

            if randy >= 500:
                self.decor.spawnDecor('ground_1',x+randwidth,randint(650,750),randint(50,300),1000,speed,'x',True)

            

            x += randint(10,1024)

            
    
            

    
        
   
    def quitter(self):
        self.cacher()
        quit()

    def test(self):
        print("ok")

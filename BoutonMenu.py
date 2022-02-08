import pygame
import Game
import json

class BoutonMenu(pygame.sprite.Sprite):
    def __init__(self,x,y,text,func,rotation=0):
        pygame.sprite.Sprite.__init__(self)
        file = open('Data/config/config.json',"r")
        self.data = json.load(file)
        file.close()
        if text == "Commencer":
            self.image1 = pygame.image.load(self.data["Items"]["panneau_menu_commencer"]["img"]).convert_alpha()
            self.image1 = pygame.transform.scale(self.image1,(self.data["Items"]["panneau_menu_commencer"]["WIDTH"]/2.5,self.data["Items"]["panneau_menu_commencer"]["HEIGHT"]/2.5))

            self.image2 = pygame.image.load(self.data["Items"]["panneau_menu_commencer_hover"]["img"]).convert_alpha()
            self.image2 = pygame.transform.scale(self.image2,(self.data["Items"]["panneau_menu_commencer_hover"]["WIDTH"]/2.5,self.data["Items"]["panneau_menu_commencer"]["HEIGHT"]/2.5))
        elif text == "Touches":
            self.image1 = pygame.image.load(self.data["Items"]["panneau_menu_touches"]["img"]).convert_alpha()
            self.image1 = pygame.transform.scale(self.image1,(self.data["Items"]["panneau_menu_touches"]["WIDTH"]/2.5,self.data["Items"]["panneau_menu_touches"]["HEIGHT"]/2.5))
            
            self.image2 = pygame.image.load(self.data["Items"]["panneau_menu_touches_hover"]["img"]).convert_alpha()
            self.image2 = pygame.transform.scale(self.image2,(self.data["Items"]["panneau_menu_touches_hover"]["WIDTH"]/2.5,self.data["Items"]["panneau_menu_touches"]["HEIGHT"]/2.5))

        elif text == "Regles":
            self.image1 = pygame.image.load(self.data["Items"]["panneau_menu_regles"]["img"]).convert_alpha()
            self.image1 = pygame.transform.scale(self.image1,(self.data["Items"]["panneau_menu_regles"]["WIDTH"]/2.5,self.data["Items"]["panneau_menu_regles"]["HEIGHT"]/2.5))
            
            self.image2 = pygame.image.load(self.data["Items"]["panneau_menu_regles_hover"]["img"]).convert_alpha()
            self.image2 = pygame.transform.scale(self.image2,(self.data["Items"]["panneau_menu_regles_hover"]["WIDTH"]/2.5,self.data["Items"]["panneau_menu_regles"]["HEIGHT"]/2.5))

        else:
            self.image1 = pygame.image.load(self.data["Items"]["panneau_menu_quitter"]["img"]).convert_alpha()
            self.image1 = pygame.transform.scale(self.image1,(self.data["Items"]["panneau_menu_quitter"]["WIDTH"]/2.5,self.data["Items"]["panneau_menu_quitter"]["HEIGHT"]/2.5))
            
            self.image2 = pygame.image.load(self.data["Items"]["panneau_menu_quitter_hover"]["img"]).convert_alpha()
            self.image2 = pygame.transform.scale(self.image2,(self.data["Items"]["panneau_menu_quitter_hover"]["WIDTH"]/2.5,self.data["Items"]["panneau_menu_quitter"]["HEIGHT"]/2.5))

        self.image = self.image1
        self.image = pygame.transform.rotate(self.image,rotation)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.func = func # Fonction mis en parametre
        self.collider = False

    def isClicked(self): # Si la souris clique sur le bouton
        mouse = pygame.mouse.get_pos()
        if self.isOverred() and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

    def isOverred(self): # Si la souris passe sur le bouton
        mouse = pygame.mouse.get_pos()
        if self.rect.colliderect((mouse[0],mouse[1],5,5)):
            return True
        else:
            return False


    def testFunc(self):
        if self.isClicked():
            Game.Game.get_instance().menu.lastClickedButton = self
            self.func()

    def updateText(self,text):
        self.image = self.fonts.render(text, True, (170, 170, 170))
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.testFunc()
        if self.isOverred():
            self.image = self.image2
        else:
            self.image = self.image1

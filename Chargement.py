import pygame
import json
import Game
class Chargement():
    def __init__(self,screen,text = ""):
        
        self.screen = screen
        f = open('Data/config/config.json',"r")
        self.data = json.load(f)
        f.close()
        self.tailleX = 600
        self.tailleY = 100
        self.image = pygame.image.load(self.data["Images"]["logo"]).convert_alpha()
        self.image = pygame.transform.scale(self.image,(400,400))
        self.fonts = pygame.font.SysFont('comicsansms', 36)
        self.barre = pygame.Rect(self.data["Settings"]["WIDTH"]/2-self.tailleX/2,3*(self.data["Settings"]["HEIGHT"])/4,self.tailleX,self.tailleY)
        self.barreCharge = pygame.Rect(self.data["Settings"]["WIDTH"]/2-self.tailleX/2+10,3*(self.data["Settings"]["HEIGHT"])/4+10,self.tailleX,self.tailleY-20)
        pygame.draw.rect(self.screen,(0,255,0),self.barre,10)
        self.update(0,text)
        


    def update(self,percent,text = ""):
        self.screen.fill((0,0,0))
        self.screen.blit(self.image,(self.data["Settings"]["WIDTH"]/2-200,100))
        pygame.draw.rect(self.screen,(0,255,0),self.barre,10)
        text_width, text_height = self.fonts.size(text)
        textToDraw = self.fonts.render(text, True, (255, 255, 255))
        apply = percent*self.tailleX/100
        self.barreCharge.width = apply
        pygame.draw.rect(self.screen,(255,0,0),self.barreCharge)
        self.screen.blit(textToDraw,(self.data["Settings"]["WIDTH"]/2-self.tailleX/2,self.barre.y-text_height-10))

        pygame.display.flip()

import pygame
import json

class Lit(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        f = open('Data/config/config.json')
        self.data = json.load(f)
        f.close()
        self.imgNoHover = pygame.image.load(self.data["Items"]["passer_la_nuit"]["img"])
        self.imgNoHover = pygame.transform.scale(self.imgNoHover,(self.data["Items"]["passer_la_nuit"]["WIDTH"],self.data["Items"]["passer_la_nuit"]["HEIGHT"]))

        self.imageHoverYes = pygame.image.load(self.data["Items"]["passer_la_nuit_oui"]["img"])
        self.imageHoverYes = pygame.transform.scale(self.imageHoverYes,(self.data["Items"]["passer_la_nuit_oui"]["WIDTH"],self.data["Items"]["passer_la_nuit_oui"]["HEIGHT"]))

        self.imageHoverNo = pygame.image.load(self.data["Items"]["passer_la_nuit_non"]["img"])
        self.imageHoverNo = pygame.transform.scale(self.imageHoverNo,(self.data["Items"]["passer_la_nuit"]["WIDTH"],self.data["Items"]["passer_la_nuit"]["HEIGHT"]))

        self.image = self.imgNoHover
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.data["Settings"]["WIDTH"]/2,self.data["Settings"]["HEIGHT"]/2)
        self.game = game
        self.collider = False
        self.isVisible = False

    def afficher(self):
        self.game.all_sprites.add(self)
        self.isVisible = True
        

    def cacher(self):
        self.game.all_sprites.remove(self)
        self.isVisible = False
        self.game.planque.isInMenu = False
    def isOverred(self):  
        mouse = pygame.mouse.get_pos()
        if self.rect.colliderect((mouse[0], mouse[1], 5, 5)) and self.isVisible:
            return True
        else:
            return False
    def isQuitting(self):
        if not self.isOverred() and pygame.mouse.get_pressed()[0] and self.isVisible:
            return True
        else:
            return False

    def noHover(self):
        self.image = self.imgNoHover

    def hoverYes(self):
        self.image = self.imageHoverYes

    def hoverNo(self):
        self.image = self.imageHoverNo

    def update(self):
        #pygame.draw.rect(self.game.screen,(255,0,0),(330,410,120,100))
        #pygame.draw.rect(self.game.screen,(255,0,0),(550,410,120,100))
        mouse = pygame.mouse.get_pos()
        if pygame.Rect(330,410,120,100).colliderect((mouse[0],mouse[1],1,1)): 
            self.image = self.imageHoverYes
            if pygame.mouse.get_pressed()[0]:
                i = 0
                for i in range(1,3):
                    if self.game.nbRun % 3 != 0:
                        self.game.nbRun+= 1
                self.game.night = True
                self.cacher() 
        elif pygame.Rect(550,410,120,100).colliderect((mouse[0],mouse[1],1,1)): 
            self.image = self.imageHoverNo
            if pygame.mouse.get_pressed()[0]:
                self.cacher()
        else:
            self.image = self.imgNoHover
        if self.isQuitting():
            self.cacher()
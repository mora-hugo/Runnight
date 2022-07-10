import pygame
import json

class Baignoire(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        f = open('Data/config/config.json')
        self.data = json.load(f)
        f.close()

        self.image = pygame.image.load(self.data["Items"]["BaignoireHUD"]["img"])
        self.image = pygame.transform.scale(self.image,(self.data["Items"]["BaignoireHUD"]["WIDTH"],self.data["Items"]["BaignoireHUD"]["HEIGHT"]))

        self.fonts = pygame.font.Font(self.data["Font"]["base"], 36)
        self.rect = self.image.get_rect()
        self.rect.center = (self.data["Settings"]["WIDTH"]/2,self.data["Settings"]["HEIGHT"]/2)
        self.game = game
        self.collider = False
        self.isVisible = False
        self.boost = 1
        self.amountLanding = 10 #montant pour augmenter
        self.amountJump = 10
        self.canBuyJump = False
        self.canBuyLanding = False



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
    #def isOverredButton(self):


    def update(self):
        #pygame.draw.rect(self.game.screen,(255,0,0),(330,410,120,100))
        #pygame.draw.rect(self.game.screen,(255,0,0),(550,410,120,100))
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect((550,410,120,100))
        
        #pygame.draw.rect(self.game.screen,(255,0,0),(410,500,220,100))
        #pygame.draw.rect(self.game.screen,(124,124,124,0),(410,500,220,100))
        if self.game.player.argent >= self.amountJump:
            self.canBuyJump = True
            self.colorJump = (0,0,0)
        else:
            self.canBuyJump = False
            self.colorJump = (255,0,0)

        if self.game.player.argent >= self.amountLanding:
            self.canBuyLanding = True
            self.colorLanding = (0,0,0)
        else:
            self.canBuyLanding= False
            self.colorLanding = (255,0,0)
        self.game.screen.blit(self.fonts.render("Ameliorer l'escalade : " + str(self.amountLanding) + "  argents", True, self.colorLanding),(300,500))   
        if pygame.Rect(290,500,400,60).colliderect((mouse[0],mouse[1],1,1)) and pygame.mouse.get_pressed()[0] and self.canBuyLanding:
            self.cacher()
            self.game.player.argent -= self.amountLanding
            self.game.player.bonusRiding += 1
            self.amountLanding = int(self.amountLanding*1.8)
        self.game.screen.blit(self.fonts.render("Ameliorer la chute : " + str(self.amountJump) + " argents", True, self.colorJump),(300,400))   
        if pygame.Rect(290,400,400,60).colliderect((mouse[0],mouse[1],1,1)) and pygame.mouse.get_pressed()[0] and self.canBuyJump:
            self.cacher()
            self.game.player.argent -= self.amountJump
            self.amountJump = int(self.amountJump*1.3)
            self.game.player.hardLandingBonus += 1
        if self.isQuitting():
            self.cacher()
        """
         if pygame.Rect(330,410,120,100).colliderect((mouse[0],mouse[1],1,1)): 
            self.image = self.imageHoverYes
            if pygame.mouse.get_pressed()[0]:
                i = 0
                self.game.nbRun+= 1
                for i in range(1,3):
                    if self.game.nbRun % 3 != 0:
                        self.game.nbRun+= 1
                self.game.night = True
                self.game.nbRun -=1
                self.cacher() 
        elif pygame.Rect(550,410,120,100).colliderect((mouse[0],mouse[1],1,1)): 
            self.image = self.imageHoverNo
            if pygame.mouse.get_pressed()[0]:
                self.cacher()
        else:
            self.image = self.imgNoHover
       
       """
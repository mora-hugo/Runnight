import pygame
import json
from ItemShowcase import ItemShowcase
import armoire
class Biblioteque(pygame.sprite.Sprite):
    def __init__(self,game,playground):
        pygame.sprite.Sprite.__init__(self)
        f = open('Data/config/config.json')
        self.data = json.load(f)
        f.close()
        self.selfData = self.data["Items"]["BibliotequeHUD"]
        self.image = pygame.image.load(self.selfData["img"]).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.selfData["WIDTH"],self.selfData["HEIGHT"]))

        self.rect = self.image.get_rect()
        self.rect.center = (self.data["Settings"]["WIDTH"]/2,self.data["Settings"]["HEIGHT"]/2)
        self.game = game
        self.collider = False
        self.isVisible = False
        self.playground = playground
        self.imgSprites = {}
        self.sprites = pygame.sprite.Group()
        self.loadSpritesImg()
        

    def loadSpritesImg(self):
        for i in self.data["Ingredients"]:
            str = "Recette_"+i
            self.imgSprites[i] = self.data["Items"][str]
            self.imgSprites[i]["img"] = pygame.image.load(self.imgSprites[i]["img"]).convert_alpha()

    def afficherIngredients(self):

        y_offset = 50
        x_offset = 250
        i = 1

        for ingredient in self.data['Ingredients']:
            self.sprites.add(ItemShowcase(self.playground.decor.ingredients[ingredient],100+x_offset,100+y_offset,ingredient,self.imgSprites[ingredient]["img"],self))

            if i % 3 == 0:
                y_offset += 110
                x_offset = 250
            else:
                x_offset += 120
            i+=1
            
    def afficher(self):
        self.afficherIngredients()
        self.game.all_sprites.add(self)
        self.game.all_sprites.add(self.sprites)
 
        
        self.isVisible = True

    def cacher(self):
        self.game.all_sprites.remove(self)
        self.game.all_sprites.remove(self.sprites)

        self.isVisible = False
        self.game.planque.isInMenu = False

    def isQuitting(self):
        if not self.isOverred() and pygame.mouse.get_pressed()[0] and self.isVisible:
            return True
        else:
            return False
    def isOverred(self):  
        mouse = pygame.mouse.get_pos()
        if pygame.Rect(301,49,414,659).colliderect((mouse[0], mouse[1], 5, 5)) and self.isVisible:
            return True
        else:
            return False
    def isQuitting(self):
        if not self.isOverred() and pygame.mouse.get_pressed()[0] and self.isVisible:
            return True
        else:
            return False

    def update(self):
        if self.isQuitting():
            print("cacher")
            self.cacher()


class ItemShowcase(pygame.sprite.Sprite):

    def __init__(self, data, x, y ,name,imgPopup,bibliotheque):
        pygame.sprite.Sprite.__init__(self)
        
        self.bibliotheque = bibliotheque
        self.image = data['img']
        self.rect = self.image.get_rect()
        self.baseX = x
        self.baseY = y
        self.rect.x = x
        self.rect.y = y
        self.rect.width = data["width"]
        self.rect.height = data["height"]
        self.recetteImg = imgPopup
        self.name = name
        self.imgPopup = imgPopup
        self.collider = False
        
        
        
    




    def isOverred(self): # Si la souris passe sur le bouton
        mouse = pygame.mouse.get_pos()
        if self.rect.colliderect((mouse[0],mouse[1],5,5)):
            return True
        else:
            return False
        #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+90, self.rect.bottom-260,50,50))
        #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+425, self.rect.bottom-260,50,50))
        #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+735, self.rect.bottom-260,50,50))

    def update(self):
        if self.isOverred():
            self.bibliotheque.game.screen.blit(self.recetteImg, (self.rect.x +10 ,self.rect.y -45))
   
       

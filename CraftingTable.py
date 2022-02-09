import pygame
import Game
import ItemShowcase
import json
class CraftingTable(pygame.sprite.Sprite):
    def __init__(self,game,decor,planque):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(game.data["Items"]["crafting_table"]["img"]).convert_alpha()
        self.image = pygame.transform.scale(self.image,(game.data["Items"]["crafting_table"]["WIDTH"]*1.5,game.data["Items"]["crafting_table"]["HEIGHT"]*1.5))
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = game.data["Settings"]["WIDTH"]/2 - game.data["Items"]["crafting_table"]["WIDTH"]/2*1.5
        self.rect.y = 10
        #self.rect.y = game.data["Settings"]["HEIGHT"]/2 - game.data["Items"]["crafting_table"]["HEIGHT"]/2*1.5
        self.collider = False
        self.sprites = pygame.sprite.Group()
        self.isCaseClicked = False
        self.caseClicked = -1
        self.decor = decor
        self.isVisible = False
        self.planque = planque
        self.createCollisionBox()
        self.cacher()
        
        

    def createCollisionBox(self):
        inventoryIngredient = self.game.player.inventory["Ingredients"]
        sortedDict = dict( sorted(inventoryIngredient.items(), key=lambda x: x[0].lower()) )
        data = self.decor.ingredients

        

        #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+47,self.rect.bottom-135,80,50))
        i = 0

        for rect in data:
            
            #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+47+110*rect,self.rect.bottom-65,80,50))
            if i==0:
                ItemShowcase.ItemShowcase(data[rect], self.rect.left+55, self.rect.bottom-135,self,i,rect)
            elif i== len(data)-1 and len(data) == 10:
                ItemShowcase.ItemShowcase(data[rect], self.rect.left+55+110*7, self.rect.bottom-145,self,i,rect)
            elif i < 9:
                ItemShowcase.ItemShowcase(data[rect], self.rect.left-43+110*i, self.rect.bottom-65,self,i,rect)
            i+=1


        #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+47+110*7,self.rect.bottom-145,80,50))
        
        self.afficher()

    def afficherIngredients(self):
        self.game.all_sprites.add(self.sprites)

    def cacherIngredients(self):
        
        self.game.all_sprites.remove(self.sprites)

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

    def afficher(self):
        self.game.all_sprites.add(self)
        self.isVisible = True
        self.planque.isInMenu = True
        self.afficherIngredients()

    def cacher(self):
        self.game.all_sprites.remove(self)
        self.isVisible = False
        self.planque.isInMenu = False
        self.cacherIngredients()

    def update(self):
        ingredient1 = None
        ingredient2 = None
        ingredient3 = None

        for case in self.sprites:
            if case.deposerSurCase:
                if case.caseDepose == 1:
                    ingredient1 = case.name
                elif case.caseDepose == 2:
                    ingredient2 = case.name
                elif case.caseDepose == 3:
                    ingredient3 = case.name
        if ingredient1 is not None and ingredient2 is not None and canCraft(ingredient1,ingredient2,ingredient3):
            pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+385, self.rect.bottom-170,120,70))
            mouse = pygame.mouse.get_pos()
            if pygame.Rect(self.rect.left+385, self.rect.bottom-170,120,70).colliderect((mouse[0],mouse[1],1,1)) and pygame.mouse.get_pressed()[0]:
                print("Plat creer !")
                creerPlat(self.game.player,ingredient1,ingredient2,ingredient3)
                for case in self.sprites:
                    if case.deposerSurCase:
                        case.kill()
        
        if self.isQuitting():
            self.cacher()

def canCraft(ingredient1, ingredient2, ingredient3=None):
    f = open('Data/config/config.json', 'r')
    data = json.load(f)
    f.close()
    for recette in data['Recettes']:
        recetteT = []

        for i in data['Recettes'][recette]:
            if data['Recettes'][recette][i] == ingredient1 and i not in recetteT:
                recetteT.append(i)
            elif data['Recettes'][recette][i] == ingredient2 and i not in recetteT:

                recetteT.append(i)
            elif ingredient3 is not None and data['Recettes'][recette][i] == ingredient3 and i not in recetteT:

                recetteT.append(i)
            if "1" in recetteT and "2" in recetteT and "3" in recetteT:
                return True
        recetteT.clear()
    return False
"""        if ingredient3 is None:
            if "1" in recetteT and "2" in recetteT:
                return True
        else:"""
            
   

def creerPlat(joueur, ingredient1, ingredient2, ingredient3=None):
    f = open('Data/config/config.json', 'r')
    data = json.load(f)
    f.close()
    for recette in data['Recettes']:
        recetteT = []

        for i in data['Recettes'][recette]:
            if data['Recettes'][recette][i] == ingredient1 and i not in recetteT:
                recetteT.append(i)
            elif data['Recettes'][recette][i] == ingredient2 and i not in recetteT:

                recetteT.append(i)
            elif ingredient3 is not None and data['Recettes'][recette][i] == ingredient3 and i not in recetteT:

                recetteT.append(i)
        if "1" in recetteT and "2" in recetteT and "3" in recetteT:
                if recette in joueur.inventory["Plats"].keys():
                    joueur.inventory["Plats"][recette] += 1
                else:
                    joueur.inventory["Plats"][recette] = 1

        """if ingredient3 is None:
            if "1" in recetteT and "2" in recetteT:
                if data['Recettes'][recette] in joueur.inventory.keys():
                    joueur.inventory[data['Recettes'][recette]] += 1
                else:
                    joueur.inventory[data['Recettes'][recette]] = 1"""
        
            
        recetteT.clear()    
import pygame
import Game
import ItemShowcase
import json
import InventoryItem
import random
class CraftingTable(pygame.sprite.Sprite):
    def __init__(self,game,decor,planque):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(game.data["Items"]["crafting_table"]["img"]).convert_alpha()
        self.image = pygame.transform.scale(self.image,(game.data["Items"]["crafting_table"]["WIDTH"]*1.5,game.data["Items"]["crafting_table"]["HEIGHT"]*1.5))
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = game.data["Settings"]["WIDTH"]/2 - game.data["Items"]["crafting_table"]["WIDTH"]/2*1.5
        self.rect.y = 10+200
        #self.rect.y = game.data["Settings"]["HEIGHT"]/2 - game.data["Items"]["crafting_table"]["HEIGHT"]/2*1.5
        self.collider = False
        self.sprites = pygame.sprite.Group()
        self.isCaseClicked = False
        self.caseClicked = -1
        self.decor = decor
        self.isVisible = False
        self.planque = planque
        self.createCollisionBox()
        self.cacherFirstTime()
        self.item = None
        

    def createCollisionBox(self):

        inventoryIngredient = self.game.player.inventory["Ingredients"]

        data = self.decor.ingredients        

        for i in data:
            data[i]["quantite"] = 0


        
        for i in inventoryIngredient:
            for y in data:
                if i == y:
                    data[y]["quantite"] = inventoryIngredient[i]

        

        #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+47,self.rect.bottom-135,80,50))
        i = 0

        for ingredient in data:
            
            #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+47+110*rect,self.rect.bottom-65,80,50))
            if i==0:
                ItemShowcase.ItemShowcase(data[ingredient], self.rect.left+55, self.rect.bottom-135,self,i,ingredient)
            elif i== len(data)-1 and len(data) == 10:
                ItemShowcase.ItemShowcase(data[ingredient], self.rect.left+55+110*7, self.rect.bottom-145,self,i,ingredient)
            elif i < 9:
                ItemShowcase.ItemShowcase(data[ingredient], self.rect.left-43+110*i, self.rect.bottom-65,self,i,ingredient)
            i+=1


        #pygame.draw.rect(self.game.screen,(255,0,0),(self.rect.left+47+110*7,self.rect.bottom-145,80,50))
        self.game.all_sprites.add(self)
        self.game.all_sprites.add(self.sprites)

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
        for sprite in  self.sprites:
            sprite.kill()
        self.createCollisionBox()
        
        
    def cacherFirstTime(self):
        self.game.all_sprites.remove(self)
        self.isVisible = False
        self.planque.isInMenu = False
        self.cacherIngredients()
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
        if ingredient1 is not None and ingredient2 is not None and ingredient3 is not None and canCraft(ingredient1,ingredient2,ingredient3):
            craft = getCraft(ingredient1,ingredient2,ingredient3)
            self.item = ItemShowcase.ItemShowcase(self.game.playground.plats[craft], self.rect.left+385, self.rect.bottom-170,self,-1,craft,True)
            self.item.isPlat = True
            self.item.isCraftable = True
            self.item.afficherCraftResult()
            mouse = pygame.mouse.get_pos()
    
            if pygame.Rect(self.rect.left+385, self.rect.bottom-170,120,70).colliderect((mouse[0],mouse[1],1,1)) and pygame.mouse.get_pressed()[0]:
                creerPlat(self.game.player,ingredient1,ingredient2,ingredient3)
                for case in self.sprites:
                    if case.deposerSurCase:
                        if case.name in  self.game.player.inventory["Ingredients"]:
                            self.game.player.inventory["Ingredients"][case.name] -= 1
                            print("Quantite : ", self.game.player.inventory["Ingredients"][case.name])
                            case.kill()
                            self.item.kill()
                self.afficher()
        

        
        elif not canCraft(ingredient1,ingredient2,ingredient3) and ingredient1 is not None and  ingredient2 is not None and  ingredient3 is not None:
            self.item = ItemShowcase.ItemShowcase(self.game.playground.plats["Soupe"], self.rect.left+385, self.rect.bottom-170,self,-1,"Soupe",True)
            self.item.isPlat = True
            self.item.isCraftable = True
            self.item.afficherCraftResult()
            mouse = pygame.mouse.get_pos()
            if pygame.Rect(self.rect.left+385, self.rect.bottom-170,120,70).colliderect((mouse[0],mouse[1],1,1)) and pygame.mouse.get_pressed()[0]:
                creerPlat(self.game.player,ingredient1,ingredient2,ingredient3,True)
                for case in self.sprites:
                    if case.deposerSurCase:
                        self.game.player.inventory["Ingredients"][case.name] -= 1
                        print("Quantite : ", self.game.player.inventory["Ingredients"][case.name])
                        case.kill()
                        self.item.kill()
                self.afficher()
        elif self.item is not None:
            self.item.kill()
            for case in self.sprites:
                if case.isPlat or case.isCraftable:
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
            
def getCraft(ingredient1, ingredient2, ingredient3=None):
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
                return recette
        recetteT.clear()
    return None

def creerPlat(joueur, ingredient1, ingredient2, ingredient3=None,isPoop=False):
    f = open('Data/config/config.json', 'r')
    data = json.load(f)
    f.close()
    if not isPoop:
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
                        
                        joueur.inventory["Plats"][recette].append(InventoryItem.InventoryItem(recette,random.uniform(0.6,1.4)*joueur.game.data["Recettes"][recette]["bonus"]["value"]*100,joueur.game.data["Recettes"][recette]["bonus"]["type"],joueur))
                        
                        
                        #else:


                    else:
                        
                        joueur.inventory["Plats"][recette] = []
                        joueur.inventory["Plats"][recette].append(InventoryItem.InventoryItem(recette,random.uniform(0.6,1.4)*joueur.game.data["Recettes"][recette]["bonus"]["value"]*100,joueur.game.data["Recettes"][recette]["bonus"]["type"],joueur))
                    print(joueur.inventory["Plats"])
            
                
            recetteT.clear()    
    else:
            temp = data["Ingredients"][ingredient1]["coef"][ingredient2]*data["Ingredients"][ingredient2]["coef"][ingredient3]*data["Ingredients"][ingredient1]["coef"][ingredient3]
            temp = random.uniform(0.6,1.4)*temp
            if "Soupe" in joueur.inventory["Plats"]:
                joueur.inventory["Plats"]["Soupe"].append(InventoryItem.InventoryItem("Soupe",temp,joueur.game.data["Ingredients"][ingredient3]["bonus"]["type"],joueur))
            else:
                joueur.inventory["Plats"]["Soupe"] = []
                joueur.inventory["Plats"]["Soupe"].append(InventoryItem.InventoryItem("Soupe",temp,joueur.game.data["Ingredients"][ingredient3]["bonus"]["type"],joueur))

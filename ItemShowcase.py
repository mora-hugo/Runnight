import pygame

class ItemShowcase(pygame.sprite.Sprite):

    def __init__(self, data, x, y,craftingTable,num,name,isPlat = False):
        pygame.sprite.Sprite.__init__(self)
        
        if isPlat or data["quantite"] > 0:
            self.image = data['img']
            self.rect = self.image.get_rect()
            self.baseX = x
            self.baseY = y
            self.rect.x = x
            self.rect.y = y
            self.rect.width = data["width"]
            self.rect.height = data["height"]
            self.num = num
            self.name = name
            self.deposerSurCase = False
            self.caseDepose = -1
            self.isPlat = False 
            self.isCraftable = False
            self.collider = False
            self.craftingTable = craftingTable
            self.afficher()
        else:
            self.kill()

    def afficherCraftResult(self):
        self.afficher()
        self.craftingTable.game.all_sprites.add(self)
    def afficher(self):
        self.craftingTable.sprites.add(self)

    def cacher(self):
        self.craftingTable.sprites.remove(self)

    def isMouseUp(self): # Si la souris clique sur le bouton
        if self.isOverred() and self.craftingTable.game.mouse_pressed == 1:
            return True
        else:
            return False

    def isMouseDown(self): # Si la souris clique sur le bouton
        if self.isOverred() and self.craftingTable.game.mouse_pressed == 0:

            return True
        else:
            return False

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
        if not self.isPlat:
            if self.isMouseDown() and not self.craftingTable.isCaseClicked:
                self.craftingTable.caseClicked = self.num
                self.craftingTable.isCaseClicked = True
            elif self.isMouseUp() and self.craftingTable.isCaseClicked and self.craftingTable.caseClicked == self.num:
                self.craftingTable.isCaseClicked = False
                self.craftingTable.caseClicked = -1
            if self.rect.colliderect((self.craftingTable.rect.left+90, self.craftingTable.rect.bottom-260,50,50)): # Deposer sur la case 1
                self.deposerSurCase = True
                self.caseDepose = 1
            elif self.rect.colliderect((self.craftingTable.rect.left+425, self.craftingTable.rect.bottom-260,50,50)):
                self.deposerSurCase = True
                self.caseDepose = 2

            elif self.rect.colliderect((self.craftingTable.rect.left+735, self.craftingTable.rect.bottom-260,50,50)):
                self.deposerSurCase = True
                self.caseDepose = 3

            else:
                self.deposerSurCase = False
                self.caseDepose = -1
                self.rect.topleft = (self.baseX,self.baseY)
            if self.craftingTable.caseClicked == self.num:
                mouse = pygame.mouse.get_pos()
                self.rect.center = mouse

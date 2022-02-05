import pygame


class Bouton(pygame.sprite.Sprite): 
    def __init__(self,x,y,text,func):
        pygame.sprite.Sprite.__init__(self)
        self.fonts = pygame.font.SysFont('comicsansms', 36)
        self.image = self.fonts.render(text, True, (170, 170, 170))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.func = func # Fonction mis en parametre

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
    def update(self):
        if self.isClicked():
            self.func()

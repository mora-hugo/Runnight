import pygame
import json
import Game as game

class DecorElement(pygame.sprite.Sprite):
    def __init__(self,element,game,x,y,width,height):
        super().__init__()

        self.image = pygame.transform.scale(element['img'],(width,height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.collider = True

    

   
            
    
        
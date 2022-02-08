import pygame
import json
import Game as game

class DecorElement(pygame.sprite.Sprite):
    def __init__(self,element,game,x,y,width,height,speed,direction,isColliding):
        super().__init__()

        self.direction = direction #x ou y : x pour horizontal et y pour vertical
        self.pos_x = x
        self.pos_y = y
        self.game = game
        self.image = pygame.transform.scale(element['img'],(width,height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.collider = isColliding
        self.speed = speed

    def update(self):
        if self.direction == 'x':
            self.pos_x -= self.speed
            if (self.pos_x < -1200 and self.speed > 0) or (self.pos_x > 1200 and self.speed < 0):
                self.kill()
        else:
            self.pos_y -= self.speed
            if (self.pos_y < -1200 and self.speed > 0) or (self.pos_y > 1200 and self.speed < 0):
                self.kill()

        

        self.rect.topleft = (self.pos_x,self.pos_y)

   
            
    
        
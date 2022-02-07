import pygame
import json
import Game as game
import DecorElement


class Decor(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()

        self.game = game

        f = open('Data/config/config.json', 'r')
        self.data = json.load(f)
        f.close()



        self.decors = {} #liste des decors chargés
        self.loadDecors()


    def loadDecors(self):
        for i in self.data['Decors']:
            print(i)
            self.decors[i['name']] = i
            print(self.decors)
            self.decors[i['name']]['img'] = pygame.image.load(self.decors[i['name']]['img']).convert_alpha()
            self.decors[i['name']]['img'] = pygame.transform.scale(self.decors[i['name']]['img'],(self.decors[i['name']]['width'],self.decors[i['name']]['height']))
            
    def spawnDecor(self,nomElement,x,y,width,height):
        decor = self.decors[nomElement]
        element = DecorElement.DecorElement(decor,self.game,x,y,width,height)
        self.game.all_sprites.add(element)
       
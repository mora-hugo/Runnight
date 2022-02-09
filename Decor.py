import pygame
import json
import Game as game
import DecorElement
import Ingredient


class Decor(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()

        self.game = game

        f = open('Data/config/config.json', 'r')
        self.data = json.load(f)
        f.close()

        self.decors = {}  # liste des decors chargés
        self.loadDecors()

        self.ingredients = {}
        self.loadIngredients()

    def loadDecors(self):
        for i in self.data['Decors']:
            print(i)
            self.decors[i['name']] = i
            print(self.decors)
            self.decors[i['name']]['img'] = pygame.image.load(
                self.decors[i['name']]['img']).convert_alpha()
            self.decors[i['name']]['img'] = pygame.transform.scale(
                self.decors[i['name']]['img'], (self.decors[i['name']]['width'], self.decors[i['name']]['height']))

    def spawnDecor(self, nomElement, x, y, width, height, speed, direction, isColliding, hitBoxX=None, hitBoxY=None, hitBoxWidth=None, hitBoxHeight=None):
        decor = self.decors[nomElement]
        element = DecorElement.DecorElement(
            decor, self.game, x, y, width, height, speed, direction, isColliding, hitBoxX, hitBoxY, hitBoxWidth, hitBoxHeight)
        self.game.all_sprites.add(element)

    def loadIngredients(self):
        for ingre in self.data["Ingredients"]:
            self.ingredients[ingre] = self.data["Ingredients"][ingre]
            self.ingredients[ingre]["img"] = pygame.image.load(
                self.data["Ingredients"][ingre]["img"]).convert_alpha()
            self.ingredients[ingre]["img"] = pygame.transform.scale(self.ingredients[ingre]["img"], (
                self.data["Ingredients"][ingre]["width"], self.data["Ingredients"][ingre]["height"]))

    def spawnIngredient(self, nomElement, x, y, width, height, speed, direction, isColliding):
        ingredient = self.ingredients[nomElement]
        element = Ingredient.Ingredient(nomElement,
                                        ingredient, self.game, x, y, speed, direction, isColliding)
        self.game.all_sprites.add(element)

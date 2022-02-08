from operator import truediv
import pygame
import json
import Game


class Recette():
    @classmethod
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

            if ingredient3 is None:
                if "1" in recetteT and "2" in recetteT:
                    if data['Recettes'][recette] in joueur.inventory.keys():
                        joueur.inventory[data['Recettes'][recette]] += 1
                    else:
                        joueur.inventory[data['Recettes'][recette]] = 1
            else:
                if "1" in recetteT and "2" in recetteT and "3" in recetteT:
                    if data['Recettes'][recette] in joueur.inventory.keys():
                        joueur.inventory[data['Recettes'][recette]] += 1
                    else:
                        joueur.inventory[data['Recettes'][recette]] = 1
            recetteT.clear()
    @classmethod
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

            if ingredient3 is None:
                if "1" in recetteT and "2" in recetteT:
                    return True
            else:
                if "1" in recetteT and "2" in recetteT and "3" in recetteT:
                    return True
            recetteT.clear()
        return False

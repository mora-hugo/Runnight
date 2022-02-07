import pygame
import Bouton as btn
import Game


class BoutonTouche(btn.Bouton):
    def __init__(self,x,y,touche,key,func):
        color = (0,0,0)
        btn.Bouton.__init__(self,x,y,touche + " : " + pygame.key.name(key),func,color)
        self.key = key
        self.touche = touche

    def updateKey(self,touche,key):
        self.updateText(touche + " : " + pygame.key.name(key))

    def testFunc(self):
        jeu = Game.Game.get_instance()
        if self.isClicked() and not jeu.isMapping:
            jeu.menu.lastClickedButton = self
            self.func()

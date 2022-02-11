import pygame
import Data.bdd_score as bdd
import time

class Classement():
    def __init__(self, jeu):
        try:
            self.bddScore = bdd.BDDSCORE()
        except Exception:
            self.bddScore = False

        if self.bddScore is not False:
            self.scores = pygame.sprite.Group()
            self.screen = jeu.screen
            self.jeu = jeu
            
        else:
            print("Pas d'acces a la bdd")

    def initSprites(self):
        """
        scores = self.bddScore.afficherScore()
        offset = 100
        i = 0
        self.scores.add(Score(200, 50, 0, 0, 0,0,True))

        for score in scores:
            
            self.scores.add(Score(200, offset, i, score, scores[score]["score"],scores[score]["run"]))
            offset += 50
            i += 1
        """
        print("ok")

    def getScores(self):
        return self.scores


class Score(pygame.sprite.Sprite):
    def __init__(self, x, y, rank, name, score,run,isTitle = False):
        pygame.sprite.Sprite.__init__(self)
        self.fonts = pygame.font.SysFont('comicsansms', 36)
        if isTitle:
            self.image = self.fonts.render(
                "Rang   Pseudo   Score  Runs", True, (255, 0, 0))
        else:
            self.image = self.fonts.render(
                str(rank+1) + "   " + name + "  :  " + str(score) + "   " +str(run), True, (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collider = False

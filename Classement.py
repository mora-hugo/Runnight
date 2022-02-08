import pygame
import Data.bdd_score as bdd


class Classement():
    def __init__(self, jeu):
        try:
            self.bddScore = bdd.BDDSCORE()
        except ValueError:
            self.bddScore = False

        if self.bddScore is not False:
            self.scores = pygame.sprite.Group()
            self.screen = jeu.screen
            self.jeu = jeu
        else:
            raise Exception("Pas d'acces a la bdd")

    def initSprites(self):

        scores = self.bddScore.afficherScore()
        offset = 100
        i = 0
        for score in scores:

            self.scores.add(Score(600, offset, i, score, scores[score]))
            offset += 50
            i += 1

    def getScores(self):
        return self.scores


class Score(pygame.sprite.Sprite):
    def __init__(self, x, y, rank, name, score):
        pygame.sprite.Sprite.__init__(self)
        self.fonts = pygame.font.SysFont('comicsansms', 36)
        self.image = self.fonts.render(
            str(rank) + " " + name + " : " + str(score), True, (170, 170, 170))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collider = False

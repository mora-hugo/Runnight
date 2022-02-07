import pygame
import Game
class Parchemin(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(game.data["Items"]["papier"]["img"]).convert_alpha()
        self.image = pygame.transform.scale(self.image,(game.data["Items"]["papier"]["WIDTH"]*1.8,game.data["Items"]["papier"]["HEIGHT"]*1.8))
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.x = game.data["Settings"]["WIDTH"]/2 - game.data["Items"]["papier"]["WIDTH"]/2*1.8
        self.rect.y = game.data["Settings"]["HEIGHT"]/2 - game.data["Items"]["papier"]["HEIGHT"]/2*1.8
        self.collider = False


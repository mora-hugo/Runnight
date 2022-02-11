import pygame
class Credits(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(game.data["Items"]["credits"]["img"]).convert_alpha()
        self.image = pygame.transform.scale(self.image,(1024, 768))
        self.rect = self.image.get_rect()
        self.game = game
        self.collider = False


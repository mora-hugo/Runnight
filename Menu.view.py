import pygame


class Menu:

    def __init__(self):
        self.afficher()

    def afficher(self):
        pygame.init()
        window = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption('WestCoast')
        background = pygame.Surface(window.get_size())
        bgImg = pygame.image.load("Data/sprites/Menubg.jpg")
        background = bgImg.convert()
        window.blit(background, (0, 0))
        pygame.display.flip()

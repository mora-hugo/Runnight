from re import X
import pygame
import json
import Sound
import armoire
import CraftingTable
import Lit
import Baignoire
import Bibliotheque
class Planque(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        file = open('Data/config/config.json', "r")
        self.data = json.load(file)
        file.close()
        self.music = Sound.Sound()
        self.backgroundJungle = pygame.image.load(
            self.data["Background_images"]["jungle_jour"]).convert_alpha()
        self.backgroundSun = pygame.image.load(
            self.data["Background_images"]["sunset"]).convert_alpha()  # NUIT fond

        self.backgroundHouse = pygame.image.load(
            self.data["Background_images"]["planque"]).convert_alpha()
        self.backgroundHouse = pygame.transform.scale(
            self.backgroundHouse, (767/1.05, 1080/1.05))
        self.image = pygame.Surface(
            (self.data["Settings"]["WIDTH"], self.data["Settings"]["HEIGHT"]))

        self.image.blit(self.backgroundSun, (0, 0))
        self.image.blit(self.backgroundJungle, (0, -200))
        self.image.blit(self.backgroundHouse, (
            self.data["Settings"]["WIDTH"]/2-767/1.05/2, self.data["Settings"]["HEIGHT"]/2-1080/1.05/2-90))
        # Chargement sprite boutons
        self.boutonsImg = {}

        self.boutonsGroup = pygame.sprite.Group()
        for boutonN in self.data["Planque_boutons"]:
            self.boutonsImg[boutonN] = pygame.image.load(
                self.data["Planque_boutons"][boutonN]["img"]).convert_alpha()
            # Afficher de base
            self.boutonsGroup.add(PlanqueButton(
                boutonN,self.boutonsImg[boutonN], self.data["Planque_boutons"][boutonN]["x"], self.data["Planque_boutons"][boutonN]["y"], self.data["Planque_boutons"][boutonN]["width"], self.data["Planque_boutons"][boutonN]["height"], self))
        self.image = self.image
        self.rect = self.image.get_rect()
        self.game = game
        self.collider = False
        self.isVisible = False

        self.isInMenu = False

        #Chargement Lit

        self.lit = Lit.Lit(self.game)
        #chargement armoire
        self.armoire = armoire.armoire(game,self)

        #chargement crafting
        self.crafting_table = CraftingTable.CraftingTable(game,self.game.decor,self)

        #Chargement baignoire
        self.baignoire = Baignoire.Baignoire(self.game)

        #Chargement biblio
        self.bib = Bibliotheque.Biblioteque(self.game,self.game.playground)
        

    def afficher(self):
        self.music.playMusic("house", None, 0.03)
        self.game.all_sprites.add(self)
        self.game.all_sprites.add(self.boutonsGroup)
        self.isVisible = True

    def cacher(self):
        self.game.all_sprites.remove(self)
        self.game.all_sprites.remove(self.boutonsGroup)
        self.isInMenu = False
        self.isVisible = False


class PlanqueButton(pygame.sprite.Sprite):
    def __init__(self, nom, img, x, y, width, height, planque):
        pygame.sprite.Sprite.__init__(self)
        self.nom = nom
        self.image = img
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.planque = planque
        self.collider = False

    def afficher(self):
        self.image.set_alpha(255)

    def cacher(self):
        self.image.set_alpha(0)

    def isClicked(self):  # Si la souris clique sur le bouton
        mouse = pygame.mouse.get_pos()
        if self.isOverred() and pygame.mouse.get_pressed()[0] and self.planque.isVisible:
            return True
        else:
            return False

    def isOverred(self):  # Si la souris passe sur le bouton
        mouse = pygame.mouse.get_pos()
        if self.rect.colliderect((mouse[0], mouse[1], 5, 5)) and self.planque.isVisible:
            return True
        else:
            return False

    def update(self):
        if self.isOverred() and not self.planque.isInMenu:
            self.afficher()
        else:
            self.cacher()

        if self.isClicked() and not self.planque.isInMenu:
            self.planque.isInMenu = True
            if self.nom == 'armoire':
                self.planque.armoire.afficher()
            if self.nom == 'cuisine':
                self.planque.crafting_table.afficher()
            if self.nom == 'lit':
                self.planque.lit.afficher()
            if self.nom == "douche":
                self.planque.baignoire.afficher()
            if self.nom == "biblioteque":
                self.planque.bib.afficher()

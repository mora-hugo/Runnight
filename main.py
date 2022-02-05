import Model.Game as game
from contextlib import nullcontext
from Data.bdd_score import BDDSCORE
import os

import pygame

jeu = game.Game.get_instance() #Creation instance jeu
jeu.menu.afficher() # Afficher le menu
try:
    bddScore = BDDSCORE()
except ValueError:
    bddScore = False

while True:
    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    jeu.all_sprites.draw(jeu.screen)
    jeu.all_sprites.update()
    pygame.display.flip()

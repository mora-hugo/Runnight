import Game as game
from contextlib import nullcontext
from Data.bdd_score import BDDSCORE
from Player import Player
import pygame



jeu = game.Game.get_instance() #Creation instance jeu
jeu.menu.afficher() # Afficher le menu






#bdd load
try:
    bddScore = BDDSCORE()
except ValueError:
    bddScore = False


#player instanciation

while True:
    #event
    for event in pygame.event.get():
        jeu.get_keys(event)
        jeu.player.action(event)
        if event.type == pygame.QUIT:
            quit()
    if jeu.isMapping :
        jeu.mapping()
    jeu.update()

import Game as game
from contextlib import nullcontext
from Data.bdd_score import BDDSCORE
from Player import Player
import pygame


print("instanciation jeu")
jeu = game.Game.get_instance() #Creation instance jeu
print("jeu ok")
jeu.menu.afficher() # Afficher le menu
clock = pygame.time.Clock()





#bdd load
#try:
#    bddScore = BDDSCORE()
#except ValueError:
#    bddScore = False
#print("bdd ok")

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
    clock.tick(60)

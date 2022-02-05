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


#player instenciation
player = Player((400,-100))
jeu.all_sprites.add(player)

while True:
    #event
    for event in pygame.event.get():
        player.action(event)
        if event.type == pygame.QUIT:
            quit() 

    jeu.update_background()
    jeu.all_sprites.draw(jeu.screen)
    jeu.all_sprites.update()
    pygame.display.flip()


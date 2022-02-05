import Model.Game as game

import pygame

jeu = game.Game.get_instance() #Creation instance jeu
jeu.menu.afficher() # Afficher le menu
while True:
    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    jeu.all_sprites.draw(jeu.screen)
    jeu.all_sprites.update()
    pygame.display.flip()

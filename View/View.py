from cgitb import grey
from tkinter import Y
from turtle import width
from pygame import *
import pygame

# dimension
width = 1024
height = 768

window = display.set_mode((width, height))
display.set_caption('West Coast Game ô')
init()

# les images
fond = image.load('Data/sprites/hugo-piment.jpg')
fond = fond.convert()
# les spritesheets

# paramètres de départ
play = True
etat = 0
# les fonctions du jeu

while play:
    for events in event.get():
        if events.type == QUIT:
            play = False
            quit()

    k = key.get_pressed()

    if etat == 0:
        bgImg = pygame.image.load("Data/sprites/Menubg.jpg")
        background = bgImg.convert()
        window.blit(background, (0, 0))
        fonts = font.SysFont('comicsansms', 36)
        btn1 = fonts.render('Jouer', True,
                            (170, 170, 170))

        btn2 = fonts.render("Niveau", True,
                            (170, 170, 170))
        btn3 = fonts.render("Changer d'avatar", True,
                            (170, 170, 170))
        btn4 = fonts.render('Quitter', False,
                            (170, 170, 170))

        y = 400
        pos = pygame.mouse.get_pos()
        pressed1 = pygame.mouse.get_pressed()[0]

        window.blit(btn1, (width/8, y))
        window.blit(btn2, (width/8, y+80))
        window.blit(btn3, (width/8, y+160))
        window.blit(btn4, (width/8, y+240))

        if btn4.get_rect().collidepoint(pos) and pressed1:
            play = False
            quit()

        if k[K_RETURN]:
            etat = 1

    if etat == 1:
        window.blit(fond, (0, 0))
        if k[K_r]:
            etat = 0
    display.flip()

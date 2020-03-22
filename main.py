import pygame
from settings import settings
from map import Pipes
from map import Background

# Initalisation du module Pygame
pygame.init()

# Variable qui va permettre de réguler les FPS
clock = pygame.time.Clock()

# Initialisation de la fenêtre
window = pygame.display.set_mode((settings['window_size'][0], settings['window_size'][1]))

# Titre de la fenêtre
pygame.display.set_caption('I.A Flappy Bird')

# Dans un soucis de simplicité et de légereté du code, stockage des images dans des variables
bg_img = pygame.image.load('imgs/bg.png')
pipe_img = pygame.image.load('imgs/pipe.png')
bird_img = pygame.image.load('imgs/bird1.png')
base_img = pygame.image.load('imgs/base.png')

# Création des objets tuyeaux et fond de carte depuis la class Map dans map.py
background = Background(base_img, bg_img, window)
pipes = Pipes(pipe_img, settings['window_size'][0])
pipes2 = Pipes(pipe_img, settings['window_size'][0] + settings['horizontal_space_btw_pipes'])

# Les variables qui sont importées depuis un autre fichier sont stockées ici, pour éviter de les importer à chaque utilisation
pipe_img_x_height = settings['pipe_img_x_height']
horizontal_space_btw_pipes = settings['horizontal_space_btw_pipes']

# La boucle de jeu principale doit être executée tant que nous sommes en jeu
isPlaying = True
speed_multiplier = 1

# On utilise une fonction de pygame qu'on stock dans une variable pour pouvoir accèder plus tard aux touches préssées
keys = pygame.key.get_pressed()

# Boucle principale, tant que le jeu est actif, cette boucle tourne
while isPlaying:
    # Régulation du nombre de répétitions de la boucle par seconde
    clock.tick(settings['fps'] * speed_multiplier)

    if speed_multiplier <= 0.2:
        speed_multiplier = 0.2

    # Capture des boutons appuyés
    for event in pygame.event.get():
        # Si nous récupérons l'évenement "quitter", on arrête la boucle de jeu principale
        if event.type == pygame.QUIT:
            isPlaying = False
        # Si on appuie sur la touche espace, l'oiseau saute
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("je saute")
            if event.key == pygame.K_RIGHT:
                speed_multiplier += .1
                print(round(speed_multiplier, 2))  # On est obligés de round() la valeur à cause des floating points
            if event.key == pygame.K_LEFT:
                speed_multiplier -= .1
                print(round(speed_multiplier, 2))
            if event.key == pygame.K_DOWN:
                speed_multiplier = 1
                print(round(speed_multiplier, 2))

    # Affichage du fond grâce à l'appel de la méthode draw_background de la class Background depuis map.py
    background.draw_background()

    # Affichage et déplacements des tuyeaux grâce à l'appel de la méthode show et move de la class Pipes depuis map.py
    pipes.show(window)
    pipes.move()

    pipes2.show(window)
    pipes2.move()

    # Déplacement et actualisation de l'affichage via les méthodes de la class Background depuis map.py
    background.move_base()
    background.draw_base()

    # Quand le premier tuyau sort de la carte:
    if pipes.x <= -pipe_img_x_height:
        otherPipePosition = pipes2.x
        # Recréation de l'objet tuyaux
        del(pipes)
        pipes = Pipes(pipe_img, otherPipePosition + horizontal_space_btw_pipes)

    # Quand le second tuyeaux sort de la carte
    if pipes2.x <= -pipe_img_x_height:
        otherPipePosition = pipes.x
        # Recréation de l'objet tuyaux2
        del(pipes2)
        pipes2 = Pipes(pipe_img, otherPipePosition + horizontal_space_btw_pipes)

    # Si la base arrive à -48px (comme elle avance), il faut la redessiner à sa position initale ; permet d'avoir un défilement infinie de la base
    if background.x <= -48:
        del(background)
        background = Background(base_img, bg_img, window)

    # Actualisation de l'affichage Pygame
    pygame.display.update()

# Si la boucle principale de jeu est finie, on doit quitter proprement le programme
pygame.quit()
print("orvaor :)")
quit()

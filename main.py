import pygame
from settings import settings
from map import Pipes
from map import Background

#initalisation du module Pygame
pygame.init()

#Variable qui va permettre de réguler les FPS
clock = pygame.time.Clock()

#Initialisation de la fenêtre
window = pygame.display.set_mode((settings['window_size'][0], settings['window_size'][1]))

#Titre de la fenêtre
pygame.display.set_caption('I.A Flappy Bird')

#Dans un soucis de simplicité et de légereté du code, stockage des images dans des variables
bg_img = pygame.image.load('imgs/bg.png')
pipe_img = pygame.image.load('imgs/pipe.png')
bird_img = pygame.image.load('imgs/bird1.png') 
base_img = pygame.image.load('imgs/base.png') 

# Création des objets tuyeaux et fond de carte depuis la class Map dans map.py
background = Background(base_img, bg_img, window)
pipes = Pipes(pipe_img, settings['window_size'][0])
pipes2 = Pipes(pipe_img, settings['window_size'][0] + settings['horizontal_space_btw_pipes'])

isPlaying = True

#Boucle principale, tant que le jeu est actif, cette boucle tourne
while isPlaying:    
    #Régulation du nb de répétitions de la boucle par secondes
    clock.tick(settings['fps'])

    #Capture des boutons appuyés
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isPlaying = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("je saute")
    
    #Affichage du fond grâce à l'appel de la méthode draw_background de la class Background depuis map.py
    background.draw_background()
    
    #Affichage et déplacements des tuyeaux grâce à l'appel de la méthode show et move de la class Pipes depuis map.py
    pipes.show(window)
    pipes.move()
        
    pipes2.show(window)
    pipes2.move()
    
    #Déplacement et actualisation de l'affichage via les méthodes de la class Background depuis map.py 
    background.move_base()
    background.draw_base()
    
    #Quand le premier tuyeau sort de la carte : 
    if pipes.x <= -settings['pipe_img_x_height']:
        otherPipePosition = pipes2.x
        #Recréation de l'objet tuyeaux
        pipes = Pipes(pipe_img, otherPipePosition + settings['horizontal_space_btw_pipes'])
    
    #Quand le second tuyeaux sort de la carte
    if pipes2.x <= -settings['pipe_img_x_height']:
        otherPipePosition = pipes.x
        #Recréation de l'objet tuyeaux2
        pipes2 = Pipes(pipe_img, otherPipePosition + settings['horizontal_space_btw_pipes'])
    
    #Si la base arrive à -48px (comme elle avance), il faut la redessiner à sa position initale ; permet d'avoir un défilement infinie de la base
    if background.x <= -48:
        background = Background(base_img, bg_img, window)
        
    #Actualisation de Pygame
    pygame.display.flip()

pygame.quit()
print("Leaving game maggle")
quit()



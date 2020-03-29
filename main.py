import pygame
from settings import settings
from map import Pipes, Background, Base
from bird import Bird
import random


# Initalisation du module Pygame
pygame.init()

collision = True

# Variable qui va permettre de réguler les FPS
clock = pygame.time.Clock()

# Initialisation de la fenêtre
window = pygame.display.set_mode((settings['window_size'][0], settings['window_size'][1]))

# Titre de la fenêtre
pygame.display.set_caption('I.A Flappy Bird')

# On récupère une image et on l'affiche en en-tête de fenêtre
icon = pygame.image.load('imgs/bird1.png')
pygame.display.set_icon(icon)

# Dans un soucis de simplicité et de légereté du code, stockage des images dans des variables
bg_img = pygame.image.load('imgs/bg2.png').convert_alpha()
pipe_img = pygame.image.load('imgs/pipe.png').convert_alpha()
bird_img = pygame.image.load('imgs/bird1.png').convert_alpha()
base_img = pygame.image.load('imgs/base.png').convert_alpha()

# Création des objets tuyaux et fond de carte depuis la class Map dans map.py
background = Background(bg_img, window)
base = Base(base_img, window)
pipes = Pipes(pipe_img, settings['window_size'][0])
pipes2 = Pipes(pipe_img, settings['window_size'][0] + settings['horizontal_space_btw_pipes'])
bird = Bird(200, 200, window)

# Les variables qui sont importées depuis un autre fichier sont stockées ici, pour éviter de les importer à chaque utilisation
pipe_img_x_height = settings['pipe_img_x_height']
horizontal_space_btw_pipes = settings['horizontal_space_btw_pipes']
vertical_space_btw_pipes = settings['vertical_space_btw_pipes']

# La boucle de jeu principale doit être executée tant que nous sommes en jeu
isPlaying = True
speed_multiplier = 1

font=pygame.font.Font("flappy-bird-font.ttf", 50)

def display_text(x, y, text, color):
    message=font.render(text, True, color)
    window.blit(message, [x,y])
    color=(0,0,0)


# On utilise une fonction de pygame qu'on stock dans une variable pour pouvoir accèder plus tard aux touches préssées
keys = pygame.key.get_pressed()

score = 0

# Boucle principale, tant que le jeu est actif, cette boucle tourne
while isPlaying:
    # Régulation du nombre de répétitions de la boucle par seconde
    clock.tick(settings['fps'] * speed_multiplier)

        # On empêche le multiplicateur de descendre trop bas, car un nombre d'IPS ne peut pas être négatif
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
                bird.jump()
            # On peut contrôler avec les flèches la vitesse du jeu
            if event.key == pygame.K_RIGHT:
                speed_multiplier += .1
                print("speed multiplier:", round(speed_multiplier, 2), end="\r")  # On est obligés de round() la valeur à cause des floating points
            if event.key == pygame.K_LEFT:
                speed_multiplier -= .1
                print("speed multiplier:", round(speed_multiplier, 2), end="\r")
            if event.key == pygame.K_DOWN:
                #speed_multiplier = 1.0
                #print("speed multiplier:", round(speed_multiplier, 2), end="\r")
                bird.y += 10
            if event.key == pygame.K_UP:
                bird.y -= 10

    
   
    # Affichage du fond grâce à l'appel de la méthode draw_background de la class Background depuis map.py
    background.draw_background()
    background.move_background()

    # Affichage et déplacements des tuyeaux grâce à l'appel de la méthode show et move de la class Pipes depuis map.py
    pipes.show(window)
    pipes.move()

    pipes2.show(window)
    pipes2.move()

    bird.show()
 
    # Déplacement et actualisation de l'affichage via les méthodes de la class Background depuis map.py
    base.move_base()
    base.draw_base()

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

    # Si la base arrive à -48px (comme elle recule), il faut la redessiner à sa position initiale ; permet d'avoir un défilement infinie de la base
    if base.x <= -48:
        del(base)
        # print('new base')
        base = Base(base_img, window)

    # Si le fond est trop à gauche, alors on le supprime et on en recréer un    
    if background.x <= -350:
        del(background)
        # print('new background')
        background = Background(bg_img, window)

    # Si l'oiseau touche le sol, on perd
    if bird.y >= 492:
        isPlaying = False 


    '''
    # Si l'oiseau n'est pas en saut, il subit la force de gravité
    if bird.isJumping == False:
        bird.y += bird.velocity
    '''

    #collision
    if collision:
        #tuyau 1
        if pipes.collide(bird, window) == True:
            if bird.y < pipes.y or bird.y > (pipes.y + vertical_space_btw_pipes):
               print('Collision 1 détéctée', random.randint(0, 99))   
        else:
            if bird.x == pipes.x:      
                score += 1     
               
        #uyeau 2  
        if pipes2.collide(bird, window) == True:
            if bird.y < pipes2.y or bird.y > (pipes2.y + vertical_space_btw_pipes):
                print('Collision 2 détéctée', random.randint(0, 99))
        else:
             if bird.x == pipes2.x:
                    score += 1
            
     
        
           

    
    '''
    COLLISION NV VERSION
    if bird.is_collided(pipes.pipe_sup) or bird.is_collided(pipes.pipe_inf):
        print(bird.is_collided(pipes.pipe_sup))  
        print(bird.is_collided(pipes.pipe_inf)) 
    '''
         
         
    #affiche le score
    display_text(260, 30, str(score), (0,0,0))
       

    # Actualisation de l'affichage Pygame
    pygame.display.update()
    
        

# Si la boucle principale de jeu est finie, on doit quitter proprement le programme
pygame.quit()
print("orvaor :)")
quit()

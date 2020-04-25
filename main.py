import pygame
from settings import settings
from map import Pipes, Background, Base
from bird import Bird
import random
import time

# Initalisation du module Pygame
pygame.init()

#INITIALISATION
#Active ou non les collisions avec les tuyau (=débug)
collision = True
gravitiy = True
# La boucle de jeu principale doit être executée tant que nous sommes en jeu
gameOver = False
isPlaying = True
speed_multiplier = 1
menu = True 
score = 0
IATraining = True

if IATraining:
    collision = False
    gravitiy = False

# Les variables qui sont importées depuis un autre fichier sont stockées ici, pour éviter de les importer à chaque utilisation
pipe_img_x_height = settings['pipe_img_x_height']
horizontal_space_btw_pipes = settings['horizontal_space_btw_pipes']
vertical_space_btw_pipes = settings['vertical_space_btw_pipes']
window_x_size = settings['window_size'][0]
window_y_size = settings['window_size'][1]
populationNumber = settings['populationNumber']

# Variable qui va permettre de réguler les FPS
clock = pygame.time.Clock()

# Initialisation de la fenêtre
window = pygame.display.set_mode((window_x_size, window_y_size))

# Titre de la fenêtre
pygame.display.set_caption('I.A Flappy Bird')

# On récupère une image et on l'affiche en en-tête de fenêtre
icon = pygame.image.load('imgs/bird1.png')
pygame.display.set_icon(icon)

# SAUVEGARDE SCORE
# Ouverture en mode append ; Cela permet de créer le fichier si il n'existe pas
scoreFile = open("score.txt", "a")
#scoreFile.close()

# Dans un soucis de simplicité et de légereté du code, stockage des images dans des variables
bg_img = pygame.image.load('imgs/bg2.png').convert_alpha()
pipe_img = pygame.image.load('imgs/pipe.png').convert_alpha()
bird_img = pygame.image.load('imgs/bird1.png').convert_alpha()
base_img = pygame.image.load('imgs/base.png').convert_alpha()

# Création des objets tuyaux et fond de carte depuis la class Map dans map.py
def createObjects():
    '''
    Créé tous les objets (2 tuyaux, le sol, le fond, et l'oiseau depuis les classes respectives)
    '''
    global background, base, pipes, pipes2, bird
    background = Background(bg_img, window)
    base = Base(base_img, window)
    pipes = Pipes(pipe_img, window_x_size)
    pipes2 = Pipes(pipe_img, window_x_size + horizontal_space_btw_pipes)
    bird = Bird(200, 200, window)
    return(background, base, pipes, pipes2, bird)

createObjects()

def displayNumber(x, y, text, color = (255, 255, 255)):
    '''
    Affiche un nombre
    '''
    # Font est une variable qui définie la police que nous voulons utiliser. Nous en avons importée une libre de droits sur internet    
    font = pygame.font.Font("flappy-bird-font.ttf", 50)
    message = font.render(text, True, color)  # On pré-rend le message pour pouvoir l'afficher
    window.blit(message, [x,y])


def displayText(x, y, text, font_size, color = (255, 255, 255)):
    '''
    Affiche un texte
    '''
    font = pygame.font.SysFont("comicsansms", font_size)
    message = font.render(text, True, color)  # On pré-rend le message pour pouvoir l'afficher
    window.blit(message, [x,y])
    
def saveScore(score):
    '''
    Enregistre le score dans le fichier score.txt
    '''
    savedScores = open('score.txt', "a")
    scoreToSave = "," + str(score)
    savedScores.write(scoreToSave)
    savedScores.close()
    print('Score sauvegardée : ', score)

def checkBestScore():
    """
    Retourne le meilleur score du fichier score.txt en tant que bestScore
    """
    with open("score.txt", 'r') as score: 
        listScore = (score.read().split(sep=","))
        
        listScoreInt = []
        for n in range(len(listScore)):
            listScoreInt.append(int(listScore[n]))
            bestScore = max(listScoreInt)    
    return bestScore

runOnce = 0
birdsPopulation = []
def generatePopulation(birdsPopulation):
    """
    Génère la population d'oiseau que l'on va entraîner. Le nombre d'oiseau dépend de la valeur choisie dans settings.py 
    """
    print('Création de la population ...')   
    while len(birdsPopulation) < populationNumber:
        randomJumpDistance = random.randint(50, 300)
        birdsPopulation.append(Bird(300, 150, window, pipe1Jump=randomJumpDistance, pipe2Jump=randomJumpDistance))     
    print('Nb d\'oiseau : ', len(birdsPopulation), '/', populationNumber)
    return birdsPopulation
        
# On utilise une fonction de pygame qu'on stock dans une variable pour pouvoir accèder plus tard aux touches préssées
keys = pygame.key.get_pressed()

titre = "Flappy Bird"
regle = "Règles: - Il faut que l'oiseau passe entre les tuyaux"
regle2 = "- Il ne faut pas que l'oiseau touche les tuyaux"
regle3 = "- A chaque tuyaux passé, +1 point"
regle4 = "- Appuyez sur espace pour sauter et lancer le jeu !"
bestScoreWithText = "Meilleur score : " 


# Boucle principale, tant que le jeu est actif, cette boucle tourne
while isPlaying:
    #MENU ACCUEIL
    if menu and not IATraining:
        # Création du fond, est des textes explicatfis
        background.draw_background() 
        base.draw_base()
        displayText(175, 25, titre, 40)
        displayText(30, 130, regle, 20)
        displayText(100, 180, regle2, 20)
        displayText(100, 230, regle3, 20)
        displayText(100, 280, regle4, 20)
        displayText(175, 380, bestScoreWithText + str(checkBestScore()), 30)
            
        #Récupération des touches préssées et événements         
        for event in pygame.event.get():
            # Si nous récupérons l'évenement "quitter", on arrête la boucle de jeu principale
            if event.type == pygame.QUIT:
                isPlaying = False
            # Si on appuie sur la touche espace, le menu s'efface et le jeu commence
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                    
        # Actualisation de l'affichage Pygame
        pygame.display.update()
    
    # JEU  
    elif gameOver == False: 
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
                    if not bird.isJumping:
                        bird.jump()
                    if bird.isJumping:
                        bird.resetJump()
                        bird.jump()
                # On peut contrôler avec les flèches la vitesse du jeu
                if event.key == pygame.K_RIGHT:
                    speed_multiplier += .1
                    print("speed multiplier:", round(speed_multiplier, 2), end="\r")  # On est obligés de round() la valeur à cause des floating points
                if event.key == pygame.K_LEFT:
                    speed_multiplier -= .1
                    print("speed multiplier:", round(speed_multiplier, 2), end="\r")
                if event.key == pygame.K_DOWN:
                    speed_multiplier = 1.0
                    print("speed multiplier:", round(speed_multiplier, 2), end="\r")

            # On est obligés de re-créer un nouvel event car le type est différents
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not bird.isJumping:
                        bird.jump()
                if bird.isJumping:
                    bird.resetJump()
                    bird.jump()

        # Affichage du fond grâce à l'appel de la méthode draw_background de la class Background depuis map.py
        background.draw_background()
        background.move_background()

        # Affichage et déplacements des tuyeaux grâce à l'appel de la méthode show et move de la class Pipes depuis map.py
        pipes.show(window)
        pipes.move()

        #Affichage du deuxième groupe de tuyau
        pipes2.show(window)
        pipes2.move()

        # Affichage de l'oiseau
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
            gameOver = True
            saveScore(score)
        
        # Si l'oiseau va au dessus de la limite de la fenêtre, on perd
        if bird.y <= 0:
            gameOver = True
            saveScore(score)

        # Si l'oiseau n'est pas en saut, il subit la force de gravité
        if gravitiy:
            if bird.isJumping == False:
                bird.y += bird.velocity

        #COLLISION
        #tuyau 1
        if pipes.collide(bird, window) == True:
            #Si l'oiseau n'est pas dans la séparation verticale des 2 tuyaux
            if bird.y < pipes.y or bird.y > (pipes.y + vertical_space_btw_pipes):
                print('Collision 1 détéctée', random.randint(0, 99))   
                if collision:
                    gameOver = True
                    saveScore(score)
            else:
                if bird.x - (pipes.x + 44) == 0:
                    score += 1
                    print('score : ', score)
            
        #tuyeau 2  
        if pipes2.collide(bird, window) == True:
            #Si l'oiseau n'est pas dans la séparation verticale des 2 tuyaux
            if bird.y < pipes2.y or bird.y > (pipes2.y + vertical_space_btw_pipes):
                print('Collision 2 détéctée', random.randint(0, 99))
                if collision:
                    gameOver = True
                    saveScore(score)
            else:        
                if bird.x - (pipes2.x + 44) == 0:
                    score += 1
                    print('score : ', score)

        # Affiche le score
        displayNumber(260, 30, str(score))     
            
        #Si le mode IA est activé
        if IATraining:
            #Lancer qu'une seule fois la création de population
            if runOnce == 0:
                generatePopulation(birdsPopulation)
                runOnce +=1
            else:
                print('Nb d\'oiseau : ', len(birdsPopulation), '/', populationNumber)        
                
            birdPipes1Distance = pipes.x - bird.x
            print('DISTANCE OISEAU TUYAU1 =', birdPipes1Distance)  
            
            birdPipes2Distance = pipes2.x - bird.x
            print('DISTANCE OISEAU TUYAU2 =', birdPipes2Distance)  

            #Si il reste une population d'oiseau
            if len(birdsPopulation) > 0:
                #Pour chaque oiseau de la population
                for uniqueBird in birdsPopulation:
                    #n est le numéro de l'index de chaque oiseau dans la liste de population
                    n = birdsPopulation.index(uniqueBird)
                # print('bird number', n, 'will jump at dist =', birdsPopulation[n].pipe1Jump)
                    #Afficher l'oiseau
                    birdsPopulation[n].show()
                    #Faire subir à chaque oiseau la gravité
                    if birdsPopulation[n].isJumping == False:
                        birdsPopulation[n].y += birdsPopulation[n].velocity
                    #Faire sauter chaque oiseau aléatoirement (=débug)
                    birdsPopulation[random.randint(0, len(birdsPopulation)-1)].jump()
                    
                    #Chaque oiseau saute quand il atteint sa personnalité
                    if(birdPipes1Distance == birdsPopulation[n].pipe1Jump):
                        birdsPopulation[n].jump()
                        print('l\'oiseau a sauté')
                    
                    #Augmente le fitness de chaque oiseau de 0.1 par frame
                    birdsPopulation[n].fitness += 0.1
                # print('fitness oiseau ', n, '=', birdsPopulation[n].fitness)
                    
                    #Enregistrement du fitness de tous les oiseaux
                    listFitness = []
                    listFitness.append(int(birdsPopulation[n].fitness))
                    bestFitness = max(listFitness)    
                # print('best fitness = ',bestFitness, 'for bird index =', listFitness.index(bestFitness))
                
                    #COLLISION tuyau 1
                    if pipes.collide(birdsPopulation[n], window) == True:
                        #Si l'oiseau n'est pas dans la séparation verticale des 2 tuyaux
                        if birdsPopulation[n].y < pipes.y or birdsPopulation[n].y > (pipes.y + vertical_space_btw_pipes):
                            # print('Collision 1 détéctée', random.randint(0, 99))   
                            birdsPopulation.pop(n)
                            # print('bird', n, 'died on first pipe')
                            n -= 1
                        else:
                            if birdsPopulation[n].x - (pipes.x + 44) == 0:
                                birdsPopulation[n].fitness += 1

                if len(birdsPopulation) > 0:            
                    #COLLISION tuyau 2
                    if pipes2.collide(birdsPopulation[n], window) == True:
                        #Si l'oiseau n'est pas dans la séparation verticale des 2 tuyaux
                        if birdsPopulation[n].y < pipes2.y or birdsPopulation[n].y > (pipes2.y + vertical_space_btw_pipes):
                            # print('Collision 1 détéctée', random.randint(0, 99))   
                            birdsPopulation.pop(n)
                            # print('bird', n, 'died on second pipe')
                            n -= 1
                        else:
                            if birdsPopulation[n].x - (pipes2.x + 44) == 0:
                                birdsPopulation[n].fitness += 1
                                



        # Actualisation de l'affichage Pygame
        pygame.display.update()   
    
    #GAME OVER
    else:
        background.draw_background() 
        base.draw_base()
        displayText(175, 100, "Game Over", 40)
        displayNumber(260, 30, str(score))
        displayText(175, 200, "Appuyez sur SPACE pour rejouer", 20)
        displayText(175, 250, "Appuyez sur ECHAP pour quitter", 20)
        
        #Le joueur a peut être fait un nouveau meilleur score, il faut donc actualiser la variable bestScore
        bestScore = checkBestScore()

        #Récupération des touches préssées et événements         
        for event in pygame.event.get():
            # Si nous récupérons l'évenement "quitter", on arrête la boucle de jeu principale
            if event.type == pygame.QUIT:
                isPlaying = False
            # Si on appuie sur la touche espace, le menu s'efface et le jeu commence
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameOver = False
                    menu = True
                    score = 0
                    createObjects()
                if event.key == pygame.K_ESCAPE:
                    isPlaying = False
                    
        # Actualisation de l'affichage Pygame
        pygame.display.update()
    


# Si la boucle principale de jeu est finie, on doit quitter proprement le programme
pygame.quit()
print("Fin du jeu :)")
quit()
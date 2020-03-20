import pygame
from settings import settings
from map import Pipes
from map import Background

pygame.init()
clock = pygame.time.Clock()

win_width = settings['window_size'][0]
win_height = settings['window_size'][1]

window = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption('I.A Flappy Bird')

bg_img = pygame.image.load('imgs/bg.png')
pipe_img = pygame.image.load('imgs/pipe.png')
bird_img = pygame.image.load('imgs/bird1.png') 
base_img = pygame.image.load('imgs/base.png') 

background = Background(base_img, bg_img, window)
pipes = Pipes(pipe_img)

isPlaying = True

while isPlaying:    
    clock.tick(settings['fps'])

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isPlaying = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("je saute")
    
    background.draw_background()
    
    pipes.show(window)
    pipes.move()
    
    background.move_base()
    background.draw_base()

    if pipes.x <= -60:
        #print('new pipes')
        pipes = Pipes(pipe_img)
        
    if background.x <= -48:
        #print('NEW BASE')
        background = Background(base_img, bg_img, window)
        
    pygame.display.flip()
    #print("ca tourne")

pygame.quit()
print("orvoar")
quit()


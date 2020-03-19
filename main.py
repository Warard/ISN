import pygame
from settings import settings
from map import Pipes

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

isPlaying = True

while isPlaying:    
    clock.tick(settings['fps'])
    
    window.blit(bg_img, (0, 0))
    window.blit(base_img, (0, 512))
    window.blit(bg_img, (288, 0))
    window.blit(base_img, (288, 512))

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isPlaying = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("je saute")

    pipes = Pipes(pipe_img)
    pipes.show(window)

    pygame.display.flip()
    print("ca tourne")

pygame.quit()
print("orvoar")
quit()


import pygame
from settings import settings

pygame.init()

win_width = settings['window_size'][0]
win_height = settings['window_size'][1]

window = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption('I.A Flappy BirdI'

pipe_img = pygame.image.load('imgs/pipe.png')
#bg_img = pygame.image.load('imgs/bg.png')
#bird_img = pygame.image.load('imgs/bird1.png') 
#base_img = pygame.image.load('imgs/base.png') 

pygame.quit()
from settings import settings
import pygame
import random

class Background():
    def __init__(self, base_img, bg_img, window):
        self.x = 0
        self.base_img = base_img
        self.bg_img = bg_img
        self.window = window
        self.speed = settings['speed']    
        
    def draw_background(self):
        self.window.blit(self.bg_img, (0, 0))
        self.window.blit(self.bg_img, (288, 0))     
    
    def draw_base(self):
        self.window.blit(self.base_img, (self.x, 512))
        self.window.blit(self.base_img, (self.x + 288, 512))
        #print('base  x position = ', self.x)
        
    def move_base(self):
        self.x -= self.speed

class Pipes():
    def __init__(self, pipe_img):
        self.x = settings['window_size'][0] 
        self.y = random.randint(settings['min_random_y_pipe_spawn'], settings['max_random_y_pipe_spawn'])
        self.speed = settings['speed']
        
        self.pipe_sup = pygame.transform.flip(pipe_img, False, True)
        self.pipe_inf = pipe_img      
          
    def show(self, window):
        window.blit(self.pipe_sup, (self.x, self.y - settings['pipe_img_height']))
        window.blit(self.pipe_inf, (self.x, self.y + settings['vertical_space_btw_pipes']))
        print('showing new pipes in x= ', self.x, 'y=', self.y)
        
    def move(self):
        self.x -= self.speed
        #print('Pipes in movements !')

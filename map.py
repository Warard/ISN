import random

class Pipe():
    def __init__(self):
        # random.randint(((settings['window_size'][1] / 100) * 20), ((settings['window_size'][1] / 100) * 80))
        self.x = 50
        self.y = 0

        
        self.pipe_sup = pygame.transsform.flip(pipe_img)
        self.pipe_inf = pipe_img      
        
        
    def show(self):
        window.blit(self.pipe_sup, (self.x, self.y))
        
      

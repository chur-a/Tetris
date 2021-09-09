import pygame

class Shell():
    def __init__(self):
        self.x_line,self.y_line = (650,0)
        self.left_rect,self.top_rect = (700,200)
        self.width_rect,self.height_rect = (240,130)
        self.rect_border_radius = 4
    def draw_line(self):
        pygame.draw.line(SCREEN,(255,255,255),(self.x_line,self.y_line),(self.x_line,self.y_line + HEIGHT),5)
    def draw_rect(self):
        pygame.draw.rect(SCREEN,(255,255,255),(self.left_rect,self.top_rect,self.width_rect,self.height_rect),width = 5,border_radius = self.rect_border_radius)
        return self.left_rect,self.top_rect




pygame.init()

WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))   
RUN_GAME = True
CLOCK = pygame.time.Clock()

while RUN_GAME:
    CLOCK.tick(20)
    pygame.event.pump()
    if pygame.event.peek(pygame.QUIT):
        RUN_GAME = False
    pygame.display.update()
        
            
            
pygame.quit()
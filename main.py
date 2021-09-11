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


class Step():
    def __init__(self,x,y,color):
        self.color = color
        self.x_1 = x
        self.y_1 = y
        self.side_cube = 30
        self.x_2 = x + self.side_cube
        self.y_2 = y
        self.x_3 = x + self.side_cube
        self.y_3 = y + self.side_cube
        self.x_4 = x + self.side_cube*2
        self.y_4 = y + self.side_cube
    def show(self):
        pygame.draw.rect(SCREEN,self.color,
                         (self.x_1, self.y_1, self.side_cube, self.side_cube))
        pygame.draw.rect(SCREEN,self.color,
                         (self.x_2, self.y_2, self.side_cube, self.side_cube))
        pygame.draw.rect(SCREEN,self.color,
                         (self.x_3, self.y_3, self.side_cube, self.side_cube))
        pygame.draw.rect(SCREEN,self.color,
                         (self.x_4, self.y_4, self.side_cube, self.side_cube))
    def move(self):
        self.y_1 += 4
        self.y_2 += 4
        self.y_3 += 4
        self.y_4 += 4
        if pygame.event.peek(pygame.KEYDOWN):
            for event in pygame.event.get(eventtype=(pygame.KEYDOWN, pygame.KEYUP)):
                if event.type == pygame.KEYDOWN:
                    if event.dict['key'] == pygame.K_RIGHT:
                        self.x_1 += 4
                        self.x_2 += 4
                        self.x_3 += 4
                        self.x_4 += 4
                    elif event.dict['key'] == pygame.K_LEFT:
                        self.x_1 -= 4
                        self.x_2 -= 4
                        self.x_3 -= 4
                        self.x_4 -= 4
                    pygame.event.post(event)
                elif event.type == pygame.KEYUP:
                    pygame.event.clear(eventtype=pygame.KEYDOWN)
            
        


pygame.init()

WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))   
RUN_GAME = True
CLOCK = pygame.time.Clock()
objec = Step(100,100,(174,122,14))

while RUN_GAME:
    SCREEN.fill((255,255,255))
    CLOCK.tick(20)
    pygame.event.pump()
    objec.show()
    objec.move()
    if pygame.event.peek(pygame.QUIT):
        RUN_GAME = False
    pygame.display.update()
        
            
            
pygame.quit()
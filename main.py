import pygame

class Shell():
    def __init__(self):
        self.x_line,self.y_line = (650,0)
        self.left_rect,self.top_rect = (700,200)
        self.width_rect,self.height_rect = (240,130)
        self.rect_border_radius = 4
    
    def draw_line(self):
        pygame.draw.line(SCREEN, (0,0,255), (self.x_line, self.y_line), (self.x_line, self.y_line + HEIGHT), 5)
        return self.x_line
    
    def draw_rect(self):
        pygame.draw.rect(SCREEN, (255,0,255), (self.left_rect, self.top_rect, self.width_rect, self.height_rect), width = 5, border_radius = self.rect_border_radius)
        return self.left_rect, self.top_rect
    
    def draw_shell(self):
        self.draw_line()
        self.draw_rect()
        return self.draw_line(), self.draw_rect()


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
        self.position = 1
        
    def show(self):
        pygame.draw.rect(SCREEN,self.color,
                         (self.x_1, self.y_1, self.side_cube, self.side_cube))
        pygame.draw.rect(SCREEN,self.color,
                         (self.x_2, self.y_2, self.side_cube, self.side_cube))
        pygame.draw.rect(SCREEN,self.color,
                         (self.x_3, self.y_3, self.side_cube, self.side_cube))
        pygame.draw.rect(SCREEN,self.color,
                         (self.x_4, self.y_4, self.side_cube, self.side_cube))
        shell = Shell()
        shell.draw_shell()
    
    def move(self):
        self.y_1 += 4
        self.y_2 += 4
        self.y_3 += 4
        self.y_4 += 4
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.x_1 += 4
            self.x_2 += 4
            self.x_3 += 4
            self.x_4 += 4
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.x_1 -= 4
            self.x_2 -= 4
            self.x_3 -= 4
            self.x_4 -= 4
            
    def turn(self):
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_SPACE and self.position == 1:
                self.x_3 = self.x_1
                self.y_3 = self.y_1
                self.x_4 = self.x_1
                self.y_4 = self.y_1 + self.side_cube
                self.x_1 += self.side_cube
                self.y_1 -= self.side_cube
                self.position = 0
            elif event.key == pygame.K_SPACE and self.position == 0:
                self.x_1 = self.x_3
                self.y_1 = self.y_3
                self.x_3 = self.x_1 + self.side_cube
                self.y_3 = self.y_1 + self.side_cube
                self.x_4 += self.side_cube*2
                self.position = 1
            pygame.event.clear()
        
    def check_collision(self):
        pass
    
    def act(self):
        self.show()
        self.move()
        self.turn()


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
    objec.act()
    if pygame.event.peek(pygame.QUIT):
        RUN_GAME = False
    pygame.display.update()
        
            
            
pygame.quit()
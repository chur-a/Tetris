import pygame

class Shell():
    def __init__(self):
        self.x_line,self.y_line = (680,0)
        self.left_rect,self.top_rect = (700,200)
        self.width_rect,self.height_rect = (240,130)
        self.rect_border_radius = 4
    
    def draw_line(self):
        pygame.draw.line(SCREEN, (0,0,255), (self.x_line, self.y_line), (self.x_line, self.y_line + HEIGHT), 5)
        return self.x_line
    
    def draw_rect(self):
        pygame.draw.rect(SCREEN, (255,0,255), (self.left_rect, self.top_rect, self.width_rect, self.height_rect), width = 5, border_radius = self.rect_border_radius)
        return self.left_rect, self.top_rect
    

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
        self.left_boarder = False
        self.right_boarder = False
        
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
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.y_1 += 44
            self.y_2 += 44
            self.y_3 += 44
            self.y_4 += 44
        else:
            self.y_1 += 4
            self.y_2 += 4
            self.y_3 += 4
            self.y_4 += 4
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not self.right_boarder:
            self.x_1 += self.side_cube
            self.x_2 += self.side_cube
            self.x_3 += self.side_cube
            self.x_4 += self.side_cube
        elif pygame.key.get_pressed()[pygame.K_LEFT] and not self.left_boarder:
            self.x_1 -= self.side_cube
            self.x_2 -= self.side_cube
            self.x_3 -= self.side_cube
            self.x_4 -= self.side_cube
            
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
                if self.right_boarder:
                    self.x_1 += self.side_cube
                    self.x_2 += self.side_cube
                    self.x_3 += self.side_cube
                    self.x_4 += self.side_cube
            elif event.key == pygame.K_SPACE and self.position == 0:
                self.x_1 = self.x_3
                self.y_1 = self.y_3
                self.x_3 = self.x_1 + self.side_cube
                self.y_3 = self.y_1 + self.side_cube
                self.x_4 += self.side_cube*2
                self.position = 1
                if self.right_boarder:
                    self.x_1 -= self.side_cube
                    self.x_2 -= self.side_cube
                    self.x_3 -= self.side_cube
                    self.x_4 -= self.side_cube
            pygame.event.clear()
        
    def check_collision(self):
        shell = Shell()
        if self.position == 1:
            if self.x_1 <= self.side_cube:
                self.left_boarder = True
            else:
                self.left_boarder = False
            if self.x_4 + self.side_cube >= shell.draw_line() - self.side_cube:
                self.right_boarder = True
            else:
                self.right_boarder = False
        elif self.position == 0:
            if self.x_3 <= self.side_cube:
                self.left_boarder = True
            else:
                self.left_boarder = False
            if self.x_1 + self.side_cube >= shell.draw_line() - self.side_cube:
                self.right_boarder = True
            else:
                self.right_boarder = False
             
    def act(self):
        self.show()
        self.check_collision()
        self.move()
        self.turn()
        
    def wait(self):
        shell = Shell()
        object_2 = Step(shell.draw_rect()[0] + shell.width_rect//2 - 1.5*self.side_cube,
                        shell.draw_rect()[1] + shell.height_rect//2 - self.side_cube,(174,122,14))
        object_2.show()
        
    def stop(self):
        if self.position == 1:
            if self.y_3 + self.side_cube < HEIGHT:
                return False
            else:
                self.y_3 = self.y_4 = HEIGHT - self.side_cube
                self.y_1 = self.y_2 = HEIGHT - 2*self.side_cube
                return True
        elif self.position == 0:
            if self.y_4 + self.side_cube < HEIGHT:
                return False
            else:
                self.y_4 = HEIGHT - self.side_cube
                self.y_3 = self.y_2 = HEIGHT - 2*self.side_cube
                self.y_1 = HEIGHT - 3*self.side_cube
                return True

    
    



pygame.init()

WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))   
RUN_GAME = True
CLOCK = pygame.time.Clock()
OBJECTS = []

objec = Step(310,-4,(174,122,14))
objec_w = Step(310,-4,(174,122,14))

while RUN_GAME:
    SCREEN.fill((255,255,255))
    CLOCK.tick(20)
    pygame.event.pump()
    
    if not objec.stop():
        objec.act()
        objec_w.wait()
    else:
        OBJECTS.append(objec)
        objec = objec_w
        objec_w = Step(310,-4,(174,122,14))
        objec.act()
        objec_w.wait()
    
    for objec_p in OBJECTS:
        objec_p.show()
    
    if pygame.event.peek(pygame.QUIT):
        RUN_GAME = False
    
    pygame.display.update()
        
            
            
pygame.quit()
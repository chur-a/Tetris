import random
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
    

class Z():
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
            self.y_1 += 30
            self.y_2 += 30
            self.y_3 += 30
            self.y_4 += 30
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
        
    def check(self):
        self.left_boarder = False
        self.right_boarder = False
        self.check_collision_borders()
        self.check_collision_objects()
    
    def check_collision_borders(self):
        shell = Shell()
        if self.position == 1:
            if self.x_1 <= self.side_cube:
                self.left_boarder = True
            if self.x_4 + self.side_cube >= shell.draw_line() - self.side_cube:
                self.right_boarder = True
        elif self.position == 0:
            if self.x_3 <= self.side_cube:
                self.left_boarder = True
            if self.x_1 + self.side_cube >= shell.draw_line() - self.side_cube:
                self.right_boarder = True
             
    def act(self):
        self.show()
        self.check()
        self.move()
        self.turn()
        
    def wait(self):
        shell = Shell()
        object_2 = Z(shell.draw_rect()[0] + shell.width_rect//2 - 1.5*self.side_cube,
                        shell.draw_rect()[1] + shell.height_rect//2 - self.side_cube,self.color)
        object_2.show()
        
    def stop_bottom(self):
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

    def check_collision_objects(self): 
        for object_packed in OBJECTS:
            Checklist_right = [object_packed.x_1,object_packed.x_2,object_packed.x_3,object_packed.x_4]
            Checklist_left = [x + self.side_cube for x in Checklist_right]
            Checklist_height = [object_packed.y_1,object_packed.y_2,object_packed.y_3,object_packed.y_4]
            for cube in enumerate(Checklist_height):
                if self.position == 1:
                    if (self.y_2 - self.side_cube < cube[1] < self.y_4 + self.side_cube and
                          (self.x_1 == Checklist_left[cube[0]] or self.x_3 == Checklist_left[cube[0]])): 
                        self.left_boarder = True
                    if (self.y_2 - self.side_cube < cube[1] < self.y_4 + self.side_cube and
                          (self.x_2 + self.side_cube == Checklist_right[cube[0]] or self.x_4 + self.side_cube == Checklist_right[cube[0]])):
                        self.right_boarder = True
                elif self.position == 0:
                    if self.y_1 - self.side_cube < cube[1] < self.y_4 + self.side_cube:
                        if self.x_1 + self.side_cube == Checklist_right[cube[0]] or self.x_4 + self.side_cube == Checklist_right[cube[0]]:
                            self.right_boarder = True
                        if self.x_3 == Checklist_left[cube[0]] or self.x_1 == Checklist_left[cube[0]]:
                            self.left_boarder = True
                            
    def stop_object(self):
        for object_packed in OBJECTS:
            Checklist_x = [object_packed.x_1,object_packed.x_2,object_packed.x_3,object_packed.x_4]
            Checklist_y = [object_packed.y_1,object_packed.y_2,object_packed.y_3,object_packed.y_4]
            if self.position == 1:
                for cube in enumerate(Checklist_x):
                    if self.x_1 == cube[1] and Checklist_y[cube[0]] <= self.y_1 + self.side_cube <= Checklist_y[cube[0]] + self.side_cube:
                        self.y_1 = self.y_2 = Checklist_y[cube[0]] - self.side_cube
                        self.y_3 = self.y_4 = self.y_1 + self.side_cube
                        return True
                    if self.x_3 == cube[1] and Checklist_y[cube[0]] <= self.y_3 + self.side_cube <= Checklist_y[cube[0]] + self.side_cube:
                        self.y_3 = self.y_4 = Checklist_y[cube[0]] - self.side_cube
                        self.y_1 = self.y_2 = self.y_3 - self.side_cube
                        return True
                    if self.x_4 == cube[1] and Checklist_y[cube[0]] <= self.y_4 + self.side_cube <= Checklist_y[cube[0]] + self.side_cube:
                        self.y_3 = self.y_4 = Checklist_y[cube[0]] - self.side_cube
                        self.y_1 = self.y_2 = self.y_3 - self.side_cube
                        return True
            elif self.position == 0:
                for cube in enumerate(Checklist_x):
                    if self.x_4 == cube[1] and Checklist_y[cube[0]] <= self.y_4 + self.side_cube <= Checklist_y[cube[0]] + self.side_cube:
                        self.y_4 = Checklist_y[cube[0]] - self.side_cube
                        self.y_3 = self.y_2 = self.y_4 - self.side_cube
                        self.y_1 = self.y_3 - self.side_cube
                        return True
                    if self.x_2 == cube[1] and Checklist_y[cube[0]] <= self.y_2 + self.side_cube <= Checklist_y[cube[0]] + self.side_cube:
                        self.y_2 = self.y_3 = Checklist_y[cube[0]] - self.side_cube
                        self.y_4 = self.y_2 + self.side_cube
                        self.y_1 = self.y_2 - self.side_cube
                        return True
        return False
                              
    def stop(self):
        if self.stop_bottom():
            return True
        elif self.stop_object():
            return True
        else:
            return False
        
    def raw_equalizer(self,mark):
        if self.y_1 < mark:
            self.y_1 += self.side_cube
        if self.y_2 < mark:
            self.y_2 += self.side_cube
        if self.y_3 < mark:
            self.y_3 += self.side_cube
        if self.y_4 < mark:
            self.y_4 += self.side_cube
    
    def raw(self):
        pass
            

class I():
    def __init__(self,x,y,color):
        self.x_1 = x
        self.y_1 = y
        self.side_cube = 30
        self.y_2 = self.y_1 + self.side_cube
        self.y_3 = self.y_2 + self.side_cube
        self.y_4 = self.y_3 + self.side_cube
        self.x_2 = self.x_3 = self.x_4 = self.x_1
        self.position = 1
        self.color = color
        self.right_boarder = False
        self.left_boarder = False
    
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
            self.y_1 += 30
            self.y_2 += 30
            self.y_3 += 30
            self.y_4 += 30
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
        
    def turn_disable(self):
        right_distance = WIDTH
        left_distance = WIDTH
        shell = Shell()
        for object_packed in OBJECTS:
            Checklist_x =[object_packed.x_1,object_packed.x_2,object_packed.x_3,object_packed.x_4]
            Checklist_y =[object_packed.y_1,object_packed.y_2,object_packed.y_3,object_packed.y_4]
            if self.position == 1:
                for cube in enumerate(Checklist_y):
                    if self.y_2 - self.side_cube <= cube[1] <= self.y_2 + self.side_cube:
                        if self.x_2 >= Checklist_x[cube[0]] + self.side_cube and left_distance > self.x_2 - (Checklist_x[cube[0]] + self.side_cube):
                            left_distance = self.x_2 - (Checklist_x[cube[0]] + self.side_cube)
                        if self.x_2 + self.side_cube <= Checklist_x[cube[0]] and right_distance > Checklist_x[cube[0]] - (self.x_2 + self.side_cube):
                            right_distance = Checklist_x[cube[0]] - (self.x_2 + self.side_cube)
            elif self.position == 0:
                for cube in enumerate(Checklist_x):
                    if ((self.x_2 == cube[1] and not self.left_boarder) or (self.x_1 == cube[1] and self.left_boarder) or
                        (self.x_4 == cube[1] and self.right_boarder)):
                        if Checklist_y[cube[0]] <= self.y_2 - self.side_cube <= Checklist_y[cube[0]] + self.side_cube:
                            return True
                        if Checklist_y[cube[0]] <= self.y_2 + self.side_cube <= Checklist_y[cube[0]] + self.side_cube:
                            return True
                        if Checklist_y[cube[0]] <= self.y_2 + 2*self.side_cube <= Checklist_y[cube[0]] + self.side_cube:
                            return True            
        if self.x_2 < left_distance:
            left_distance = self.x_2
        if shell.draw_line() - self.x_2 + self.side_cube < right_distance:
            right_distance = shell.draw_line() - self.x_2 + self.side_cube
        if left_distance + right_distance <= 3*self.side_cube:
            return True
        else:
            return False
    
    def turn(self):
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_SPACE and self.position == 1:
                self.y_1 = self.y_3 = self.y_4 = self.y_2
                self.x_1 -= self.side_cube
                self.x_3 += self.side_cube
                self.x_4 += 2*self.side_cube
                self.position = 0
                if self.right_boarder == True:
                    self.x_1 -= 2*self.side_cube
                    self.x_2 -= 2*self.side_cube
                    self.x_3 -= 2*self.side_cube
                    self.x_4 -= 2*self.side_cube
                elif self.left_boarder == True:
                    self.x_1 += self.side_cube
                    self.x_2 += self.side_cube
                    self.x_3 += self.side_cube
                    self.x_4 += self.side_cube
            elif event.key == pygame.K_SPACE and self.position == 0:
                self.x_1 = self.x_3 = self.x_4 = self.x_2
                self.y_1 -= self.side_cube
                self.y_3 += self.side_cube
                self.y_4 += 2*self.side_cube
                self.position = 1
                if self.right_boarder == True:
                    self.x_1 += 2*self.side_cube
                    self.x_2 += 2*self.side_cube
                    self.x_3 += 2*self.side_cube
                    self.x_4 += 2*self.side_cube
                elif self.left_boarder == True:
                    self.x_1 -= self.side_cube
                    self.x_2 -= self.side_cube
                    self.x_3 -= self.side_cube
                    self.x_4 -= self.side_cube
                
    
    def act(self):
        self.show()
        self.check()
        self.move()
        if not self.turn_disable():
            self.turn()
        
    def wait(self):
        shell = Shell()
        object_w = I(shell.draw_rect()[0] + shell.width_rect//2 - self.side_cube//2,
                        shell.draw_rect()[1] + shell.height_rect//2 - 2*self.side_cube,(self.color))
        object_w.show()
    
    def equalization(self,level):
        if self.position == 1:
            self.y_4 = level - self.side_cube
            self.y_3 = self.y_4 - self.side_cube
            self.y_2 = self.y_3 - self.side_cube
            self.y_1 = self.y_2 - self.side_cube
        elif self.position == 0:
            self.y_1 = self.y_2 = self.y_3 = self.y_4 = level - self.side_cube
    
    def stop_bottom(self):
        if self.position == 1:
            if self.y_4 + self.side_cube < HEIGHT:
                return False
            else:
                self.equalization(HEIGHT)
                return True
        elif self.position == 0:
            if self.y_1 + self.side_cube < HEIGHT:
                return False
            else:
                self.equalization(HEIGHT)
                return True
            
    def stop_object(self):
        for object_packed in OBJECTS:
            Checklist_x = [object_packed.x_1,object_packed.x_2,object_packed.x_3,object_packed.x_4]
            Checklist_y = [object_packed.y_1,object_packed.y_2,object_packed.y_3,object_packed.y_4]
            if self.position == 1:
                for cube in enumerate(Checklist_x):
                    if self.x_4 == cube[1] and Checklist_y[cube[0]] <= self.y_4 + self.side_cube < Checklist_y[cube[0]] + self.side_cube:
                        self.equalization(Checklist_y[cube[0]])
                        return True
            elif self.position == 0:
                for cube in enumerate(Checklist_x):
                    if Checklist_y[cube[0]] <= self.y_4 + self.side_cube < Checklist_y[cube[0]] + self.side_cube:
                        if cube[1] in [self.x_1,self.x_2,self.x_3,self.x_4]:
                            self.equalization(Checklist_y[cube[0]])
                            return True
        return False
    
    def stop(self):
        if self.stop_bottom() or self.stop_object():
            return True
        else:
            return False
        
    def check_collision_borders(self):
        shell = Shell()
        if self.x_1 <= self.side_cube:
            self.left_boarder = True
        if self.x_4 + self.side_cube >= shell.draw_line() - self.side_cube:
            self.right_boarder = True
    
    def check_collision_objects(self):
        for object_packed in OBJECTS:
            Checklist_r = [object_packed.x_1,object_packed.x_2,object_packed.x_3,object_packed.x_4]
            Checklist_l = [x + self.side_cube for x in Checklist_r]
            Checklist_height = [object_packed.y_1,object_packed.y_2,object_packed.y_3,object_packed.y_4]
            for cube in enumerate(Checklist_height):
                if self.position == 1 and (self.y_1 - self.side_cube < cube[1] < self.y_4 + self.side_cube):
                    if Checklist_r[cube[0]] == self.x_1 + self.side_cube:
                        self.right_boarder = True
                    if Checklist_l[cube[0]] == self.x_1:
                        self.left_boarder = True
                elif self.position == 0 and (self.y_1 - self.side_cube < cube[1] < self.y_4 + self.side_cube):
                    if Checklist_r[cube[0]] == self.x_4 + self.side_cube:
                        self.right_boarder = True
                    if Checklist_l[cube[0]] == self.x_1:
                        self.left_boarder = True
    
    def check(self):
        self.left_boarder = False
        self.right_boarder = False
        self.check_collision_borders()
        self.check_collision_objects()
        
    def raw(self):
        if self.position == 1:
            rawcube_1 = [('self1',self.y_1)]
            rawcube_2 = [('self2',self.y_2)]
            rawcube_3 = [('self3',self.y_3)]
            rawcube_4 = [('self4',self.y_4)]
        elif self.position == 0:
            rawcube_1 = rawcube_2 = rawcube_3 = rawcube_4 = [('self1',self.y_1),('self2',self.y_2),('self3',self.y_3),('self4',self.y_4)]
        for object_packed in enumerate(OBJECTS):
            Checklist_y = [object_packed[1].y_1,object_packed[1].y_2,object_packed[1].y_3,object_packed[1].y_4]
            for i in range(len(Checklist_y)):
                if Checklist_y[i] == self.y_1:
                    rawcube_1.append((object_packed[0],i))
                elif Checklist_y[i] == self.y_2:
                    rawcube_2.append((object_packed[0],i))
                elif Checklist_y[i] == self.y_3:
                    rawcube_3.append((object_packed[0],i))
                elif Checklist_y[i] == self.y_4:
                    rawcube_4.append((object_packed[0],i))
      
        if len(rawcube_1) == 22:
            self.raw_equalization(self.y_1)
            self.raw_rect(self.y_1)
            self.raw_eliminate(rawcube_1)
            return True
        elif len(rawcube_2) == 22:
            self.raw_equalization(self.y_2)
            self.raw_rect(self.y_2)
            self.raw_eliminate(rawcube_2)
            return True
        elif len(rawcube_3) == 22:
            self.raw_equalization(self.y_3)
            self.raw_rect(self.y_3)
            self.raw_eliminate(rawcube_3)
            return True
        elif len(rawcube_4) == 22:
            self.raw_equalization(self.y_4)
            self.raw_rect(self.y_4)
            self.raw_eliminate(rawcube_4)
            return True
          
    def raw_equalization(self,mark):
        for object_packed in OBJECTS:
            object_packed.show()
            object_packed.raw_equalizer(mark)
        
        self.show()
        self.raw_equalizer(mark)
    
    def raw_eliminate(self,eleminate_list):  
        for eleminate in eleminate_list:
            if eleminate[0] == 'self1':
                self.y_1 += 1000000
            elif eleminate[0] == 'self2':
                self.y_2 += 1000000
            elif eleminate[0] == 'self3':
                self.y_3 += 1000000
            elif eleminate[0] == 'self4':
                self.y_4 += 1000000
            else:
                object_packed = OBJECTS[eleminate[0]]
                if eleminate[1] == 0:
                    object_packed.y_1 += 1000000
                elif eleminate[1] == 1:
                    object_packed.y_2 += 1000000
                elif eleminate[1] == 2:
                    object_packed.y_3 += 1000000
                elif eleminate[1] == 3:
                    object_packed.y_4 += 1000000

        
    def raw_equalizer(self,mark):
        if self.y_1 < mark:
            self.y_1 += self.side_cube
        if self.y_2 < mark:
            self.y_2 += self.side_cube
        if self.y_3 < mark:
            self.y_3 += self.side_cube
        if self.y_4 < mark:
            self.y_4 += self.side_cube
    
    def raw_rect(self,mark):
        pygame.draw.rect(SCREEN,(0,0,0),(10,mark,660,self.side_cube))
            

pygame.init()

WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))   
RUN_GAME = True
CLOCK = pygame.time.Clock()
OBJECTS = []
FIGURES = [Z(310,-4,(174,122,14)),I(310,-4,(40,25,77))]


objec = I(310,-4,(40,25,77))
objec_wait = Z(310,-4,(174,122,14))

while RUN_GAME:
    SCREEN.fill((255,255,255))
    CLOCK.tick(20)
    pygame.event.pump()

    
    if not objec.stop():
        objec.act()
        objec_wait.wait()
    else:
        if objec.raw():
            shell = Shell()
            shell.draw_line()
            shell.draw_rect()
            objec_wait.wait()
            pygame.display.update()
            pygame.time.wait(2000)
        OBJECTS.append(objec)
        objec = objec_wait
        objec_wait = random.choice([Z(310,-4,(174,122,14)),I(310,-4,(40,25,77))])
        objec.act()
        objec_wait.wait()
    
    
    for objec_packed in OBJECTS:
        objec_packed.show()
    
    if pygame.event.peek(pygame.QUIT):
        RUN_GAME = False
    
    pygame.display.update()
    

            
            
pygame.quit()
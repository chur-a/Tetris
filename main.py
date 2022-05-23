import random
import pygame


class Shell:

    def draw_line(self):
        pygame.draw.line(SCREEN, (0, 0, 255), (X_LINE, Y_LINE), (X_LINE, Y_LINE + HEIGHT), 5)
        return X_LINE

    def draw_rect(self):
        pygame.draw.rect(SCREEN, (255, 0, 255), (LEFT_RECT, TOP_RECT, WIDTH_RECT, HEIGHT_RECT),
                         width=5, border_radius=RECT_BORDER_RADIUS)
        return LEFT_RECT, TOP_RECT


class Figures(Shell):
    def show(self):
        pygame.draw.rect(SCREEN, self.color,
                         (self.x_1, self.y_1, self.side_cube, self.side_cube))
        pygame.draw.rect(SCREEN, self.color,
                         (self.x_2, self.y_2, self.side_cube, self.side_cube))
        pygame.draw.rect(SCREEN, self.color,
                         (self.x_3, self.y_3, self.side_cube, self.side_cube))
        pygame.draw.rect(SCREEN, self.color,
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
        if (pygame.key.get_pressed()[pygame.K_RIGHT] and not self.right_boarder and
         not pygame.key.get_pressed()[pygame.K_DOWN]):
            self.x_1 += self.side_cube
            self.x_2 += self.side_cube
            self.x_3 += self.side_cube
            self.x_4 += self.side_cube
        elif (pygame.key.get_pressed()[pygame.K_LEFT] and not self.left_boarder and
         not pygame.key.get_pressed()[pygame.K_DOWN]):
            self.x_1 -= self.side_cube
            self.x_2 -= self.side_cube
            self.x_3 -= self.side_cube
            self.x_4 -= self.side_cube

    def wait(self):
        object_w = self.__class__(self.x_wait, self.y_wait,(self.color))
        object_w.show()

    def stop(self):
        if self.stop_bottom() or self.stop_object():
            return True
        return False

    def stop_bottom(self):
        for cube_y in [self.y_1, self.y_2, self.y_3, self.y_4]:
            if cube_y + self.side_cube >= HEIGHT:
                self.equalization(HEIGHT, cube_y)
                return True
        return False

    def check_stop_cube(self, object_cube_x, object_cube_y, checked_cube_x, checked_cube_y):
        if (checked_cube_y <= object_cube_y + self.side_cube < checked_cube_y + self.side_cube and
                checked_cube_x == object_cube_x):
            return True
        return False

    def stop_object(self):
        for object_packed in OBJECTS:
            Checklist = [(object_packed.x_1, object_packed.y_1),
                         (object_packed.x_2, object_packed.y_2),
                         (object_packed.x_3, object_packed.y_3),
                         (object_packed.x_4, object_packed.y_4)]
            for x, y in [(self.x_1, self.y_1), (self.x_2, self.y_2), (self.x_3, self.y_3), (self.x_4, self.y_4)]:
                for check_x, check_y in Checklist:
                    if self.check_stop_cube(x, y, check_x, check_y):
                        self.equalization(check_y, y)
                        return True

    def act(self):
        self.show()
        self.check()
        self.move()
        if not self.turn_disable():
            self.turn()

    def check(self):
        self.left_boarder = False
        self.right_boarder = False
        self.check_collision_objects()
        self.check_collision_borders()

    def check_on_cube(self, object_cube_x, object_cube_y, checked_cube_x, checked_cube_y):
        if (checked_cube_y < object_cube_y + self.side_cube < checked_cube_y + 2*self.side_cube and
                checked_cube_x == abs(object_cube_x + self.side_cube)):
            return True
        return False

    def check_collision_objects(self):
        for object_packed in OBJECTS:
            Checklist_x = [object_packed.x_1, object_packed.x_2, object_packed.x_3, object_packed.x_4]
            Checklist_y = [object_packed.y_1, object_packed.y_2, object_packed.y_3, object_packed.y_4]
            for cube in enumerate(Checklist_x):
                if (
                        self.check_on_cube(self.x_2, self.y_2, cube[1], Checklist_y[cube[0]]) or
                        self.check_on_cube(self.x_1, self.y_1, cube[1], Checklist_y[cube[0]]) or
                        self.check_on_cube(self.x_3, self.y_3, cube[1], Checklist_y[cube[0]]) or
                        self.check_on_cube(self.x_4, self.y_4, cube[1], Checklist_y[cube[0]])
                ):
                    self.right_boarder = True
                if (
                        self.check_on_cube(-self.x_2, self.y_2, cube[1], Checklist_y[cube[0]]) or
                        self.check_on_cube(-self.x_1, self.y_1, cube[1], Checklist_y[cube[0]]) or
                        self.check_on_cube(-self.x_3, self.y_3, cube[1], Checklist_y[cube[0]]) or
                        self.check_on_cube(-self.x_4, self.y_4, cube[1], Checklist_y[cube[0]])
                ):
                    self.left_boarder = True

    def check_collision_borders(self):
        for x in [self.x_1, self.x_2, self.x_3, self.x_4]:
            if x <= self.side_cube:
                self.draw_line()
                self.left_boarder = True
                break
            elif x + self.side_cube >= self.draw_line() - self.side_cube:
                self.right_boarder = True
                break

    def equalization(self, level, cube_level):
        diff = cube_level + self.side_cube - level
        for y in [self.y_1, self.y_2, self.y_3, self.y_4]:
            y -= diff

    def raw(self):  #FIXME
        rawcube_1 = rawcube_2 = rawcube_3 = rawcube_4 = []
        for object_packed in enumerate(OBJECTS):
            Checklist_y = [object_packed[1].y_1, object_packed[1].y_2, object_packed[1].y_3, object_packed[1].y_4]
            for i in range(len(Checklist_y)):
                if Checklist_y[i] == self.y_1:
                    rawcube_1.append((object_packed[0], i))
                elif Checklist_y[i] == self.y_2:
                    rawcube_2.append((object_packed[0], i))
                elif Checklist_y[i] == self.y_3:
                    rawcube_3.append((object_packed[0], i))
                elif Checklist_y[i] == self.y_4:
                    rawcube_4.append((object_packed[0], i))

        rawcomplete = False

        for rawlist in sorted([rawcube_1, rawcube_2, rawcube_3, rawcube_4],
                              key=lambda item: item[0][1]):
            if len(rawlist) == 22:
                self.raw_equalization(rawlist[0][1])
                self.raw_rect(rawlist[0][1])
                self.raw_eliminate(rawlist)
                self.raw_show()
                Game.score += 10
                rawcomplete = True
        if rawcomplete:
            return True
        else:
            return False

    def raw_equalization(self, mark):
        for object_packed in OBJECTS:
            object_packed.show()
            object_packed.raw_equalizer(mark)

        self.show()
        self.raw_equalizer(mark)

    def raw_eliminate(self, eleminate_list):
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

        eleminate_list.clear()

    def raw_equalizer(self, mark):
        if self.y_1 < mark:
            self.y_1 += self.side_cube
        if self.y_2 < mark:
            self.y_2 += self.side_cube
        if self.y_3 < mark:
            self.y_3 += self.side_cube
        if self.y_4 < mark:
            self.y_4 += self.side_cube

    def raw_rect(self, mark):
        pygame.draw.rect(SCREEN, (0, 0, 0), (10, mark, 660, self.side_cube))

    def raw_show(self):
        self.draw_line()
        self.draw_rect()
        objec_wait.wait()
        Game.blit_score_table((740, 800))
        pygame.display.update()
        pygame.time.wait(2000)


class Z(Figures):
    def __init__(self, x, y, color):
        self.color = color
        self.x_1 = x
        self.y_1 = y
        self.side_cube = 30
        self.x_2 = x + self.side_cube
        self.y_2 = y
        self.x_3 = x + self.side_cube
        self.y_3 = y + self.side_cube
        self.x_4 = x + 2*self.side_cube
        self.y_4 = y + self.side_cube
        self.position = 1
        self.left_boarder = False
        self.right_boarder = False
        self.x_wait = self.draw_rect()[0] + WIDTH_RECT//2 - 1.5*self.side_cube
        self.y_wait = self.draw_rect()[1] + HEIGHT_RECT//2 - self.side_cube

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
                    
    def turn_disable(self):
        for object_packed in OBJECTS:
            Checklist_x =[object_packed.x_1,object_packed.x_2,object_packed.x_3,object_packed.x_4]
            Checklist_y =[object_packed.y_1,object_packed.y_2,object_packed.y_3,object_packed.y_4]
            if self.position == 1:
                for cube in enumerate(Checklist_x):
                    if ((cube[1] - self.side_cube < self.x_2 < cube[1] + self.side_cube) and
                     (Checklist_y[cube[0]] < self.y_2 - self.side_cube < Checklist_y[cube[0]] + self.side_cube)):
                        return True
            elif self.position == 0:
                for cube in enumerate(Checklist_x):
                    if (not self.right_boarder and self.y_4 - 4 <= Checklist_y[cube[0]] < self.y_4 + self.side_cube and
                      cube[1] == self.x_2 + self.side_cube):
                        return True
                    if self.left_boarder and self.right_boarder:
                        return True
        return False
        

class I(Figures):
    def __init__(self, x, y, color):
        self.x_1 = x
        self.y_1 = y
        self.side_cube = 30
        self.y_2 = self.y_1 + self.side_cube
        self.y_3 = self.y_2 + self.side_cube
        self.y_4 = self.y_3 + self.side_cube
        self.x_2 = self.x_3 = self.x_4 = self.x_1
        self.position = 1
        self.color = color
        self.left_boarder = False
        self.right_boarder = False
        self.x_wait = self.draw_rect()[0] + WIDTH_RECT//2 - self.side_cube//2
        self.y_wait = self.draw_rect()[1] + HEIGHT_RECT//2 - 2*self.side_cube
        
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
                if self.right_boarder_1:
                    self.x_1 -= 2*self.side_cube
                    self.x_2 -= 2*self.side_cube
                    self.x_3 -= 2*self.side_cube
                    self.x_4 -= 2*self.side_cube
                elif self.right_boarder_2:
                    self.x_1 -= self.side_cube
                    self.x_2 -= self.side_cube
                    self.x_3 -= self.side_cube
                    self.x_4 -= self.side_cube
                elif self.left_boarder:
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
                if self.right_boarder_1:
                    self.x_1 += 2*self.side_cube
                    self.x_2 += 2*self.side_cube
                    self.x_3 += 2*self.side_cube
                    self.x_4 += 2*self.side_cube
                elif self.left_boarder:
                    self.x_1 -= self.side_cube
                    self.x_2 -= self.side_cube
                    self.x_3 -= self.side_cube
                    self.x_4 -= self.side_cube
    

class J(Figures):
    def __init__(self, x, y, color):
        self.color = color
        self.x_1 = x
        self.y_1 = y
        self.side_cube = 30
        self.x_2 = self.x_1
        self.y_2 = self.y_1 + self.side_cube
        self.x_3 = self.x_2 + self.side_cube
        self.y_3 = self.y_2
        self.x_4 = self.x_3 + self.side_cube
        self.y_4 = self.y_3
        self.position = 1
        self.x_wait = self.draw_rect()[0] + WIDTH_RECT//2 - 3*self.side_cube//2
        self.y_wait = self.draw_rect()[1] + HEIGHT_RECT//2 - self.side_cube
            
    def turn_disable(self):
        for object_packed in OBJECTS:
            Checklist_x =[object_packed.x_1,object_packed.x_2,object_packed.x_3,object_packed.x_4]
            Checklist_y =[object_packed.y_1,object_packed.y_2,object_packed.y_3,object_packed.y_4]
            if self.position == 1:
                for cube in enumerate(Checklist_x):
                    if (cube[1] in [self.x_1,self.x_3] and
                          self.y_1 - self.side_cube < Checklist_y[cube[0]] + self.side_cube < self.y_1):
                        return True
            elif self.position == 2:
                for cube in enumerate(Checklist_x):
                    if (self.y_3 - self.side_cube < Checklist_y[cube[0]] < self.y_4 + self.side_cube and
                          cube[1] == self.x_3 + 2*self.side_cube):
                        return True
            elif self.position == 3:
                for cube in enumerate(Checklist_x):
                    if (cube[1] == self.x_3 and
                          self.y_3 < Checklist_y[cube[0]] - self.side_cube < self.y_3 + self.side_cube):
                        return True
            elif self.position == 4:
                for cube in enumerate(Checklist_x):
                    if (self.y_2 - self.side_cube < Checklist_y[cube[0]] < self.y_2 + self.side_cube and
                          cube[1] == self.x_2 + self.side_cube):
                        return True
        return False
    
    def turn(self):
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_SPACE and self.position == 1:
                self.x_1 += self.side_cube
                self.y_1 -= self.side_cube
                self.y_2 -= 2*self.side_cube
                self.x_3 -= self.side_cube
                self.y_3 -= self.side_cube
                self.x_4 -= 2*self.side_cube
                self.position = 2
            elif event.key == pygame.K_SPACE and self.position == 2:
                self.x_1 += self.side_cube
                self.y_1 += 2*self.side_cube
                self.x_2 += 2*self.side_cube
                self.y_2 += self.side_cube
                self.x_3 += self.side_cube
                self.y_4 -= self.side_cube
                self.position = 3
            elif event.key == pygame.K_SPACE and self.position == 3:
                self.x_1 -= 2*self.side_cube
                self.x_2 -= self.side_cube
                self.y_2 += self.side_cube
                self.x_4 += self.side_cube
                self.y_4 -= self.side_cube
                self.position = 4
            elif event.key == pygame.K_SPACE and self.position == 4:
                self.y_1 -= self.side_cube
                self.x_2 -= self.side_cube
                self.y_3 += self.side_cube
                self.x_4 += self.side_cube
                self.y_4 += 2*self.side_cube
                self.position = 1


class S(Figures):
    def __init__(self, x, y, color):
        self.color = color
        self.x_1 = x
        self.y_1 = y
        self.side_cube = 30
        self.x_2 = x - self.side_cube
        self.y_2 = y
        self.x_3 = x - self.side_cube
        self.y_3 = y + self.side_cube
        self.x_4 = x - 2*self.side_cube
        self.y_4 = y + self.side_cube
        self.position = 1
        self.x_wait = self.draw_rect()[0] + WIDTH_RECT // 2 + self.side_cube // 2
        self.y_wait = self.draw_rect()[1] + HEIGHT_RECT // 2 - self.side_cube
            
    def turn(self):
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_SPACE and self.position == 1:
                self.x_4 = self.x_3
                self.x_2 = self.x_1 = self.x_3 - self.side_cube
                self.y_3 = self.y_2
                self.y_1 -= self.side_cube
                self.position = 0
            elif event.key == pygame.K_SPACE and self.position == 0:
                self.x_1 += 2*self.side_cube
                self.x_2 = self.x_3
                self.x_4 -= self.side_cube
                self.y_1 += self.side_cube
                self.y_3 += self.side_cube
                self.position = 1
                self.turn_adjustment(self.right_flag)

    def turn_adjustment(self, right_flag):
        shell = Shell()
        if (
            right_flag or
            self.x_1 + self.side_cube > shell.draw_line()
        ):
            self.x_1 -= self.side_cube
            self.x_2 -= self.side_cube
            self.x_3 -= self.side_cube
            self.x_4 -= self.side_cube

    def turn_disable(self):
        self.left_flag = False
        self.right_flag = False
        for object_packed in OBJECTS:
            Checklist_x =[object_packed.x_1,object_packed.x_2,object_packed.x_3,object_packed.x_4]
            Checklist_y =[object_packed.y_1,object_packed.y_2,object_packed.y_3,object_packed.y_4]
            if self.position == 1:
                for cube in enumerate(Checklist_x):
                    if (Checklist_y[cube[0]] <= self.y_2 - self.side_cube < Checklist_y[cube[0]] + self.side_cube and
                        cube[1] == self.x_2 - self.side_cube):
                         return True
            elif self.position == 0:
                for cube in enumerate(Checklist_x):
                    if self.check_on_cube(-self.x_4, self.y_4, cube[1], Checklist_y[cube[0]]):
                        return True
                    if self.check_on_cube(self.x_3, self.y_3, cube[1], Checklist_y[cube[0]]):
                        self.right_flag = True
                    elif self.check_on_cube(-(self.x_4 - self.side_cube), self.y_4, cube[1], Checklist_y[cube[0]]):
                        self.left_flag = True
                    if self.left_flag and self.right_flag:
                        return True
        return False


class T(Figures):

    def __init__(self, x, y, color):
        self.color = color
        self.side_cube = 30
        self.x_1 = x
        self.y_1 = y
        self.x_2 = x - self.side_cube
        self.y_2 = y - self.side_cube
        self.x_3 = x
        self.y_3 = y - self.side_cube
        self.x_4 = x + self.side_cube
        self.y_4 = y - self.side_cube
        self.position = 1
        self.x_wait = self.draw_rect()[0] + WIDTH_RECT // 2 - self.side_cube // 2
        self.y_wait = self.draw_rect()[1] + HEIGHT_RECT // 2

    def turn(self):
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_SPACE and self.position == 1:
                self.x_1 -= self.side_cube
                self.x_2 = self.x_4 = self.x_3
                self.y_1 -= self.side_cube
                self.y_2 -= self.side_cube
                self.y_4 += self.side_cube
                self.position = 2
            elif event.key == pygame.K_SPACE and self.position == 2:
                self.x_1 += self.side_cube
                self.x_2 += self.side_cube
                self.x_4 -= self.side_cube
                self.y_2 += 2*self.side_cube
                self.y_3 += self.side_cube
                self.position = 3
            elif event.key == pygame.K_SPACE and self.position == 3:
                self.x_2 = self.x_3 = self.x_4
                self.y_3 -= self.side_cube
                self.y_4 -= 2*self.side_cube
                self.position = 4
            elif event.key == pygame.K_SPACE and self.position == 4:
                self.x_3 += self.side_cube
                self.x_4 += 2*self.side_cube
                self.y_1 += self.side_cube
                self.y_2 = self.y_4 = self.y_3
                self.position = 1
            self.turn_adjustments(self.left_flag, self.right_flag, event)

    def turn_adjustments(self, left_flag, right_flag, event):
        if event.key == pygame.K_SPACE:
            shell = Shell()
            if right_flag and self.position != 4 or self.x_1 + 2*self.side_cube > shell.draw_line():
                self.x_1 -= self.side_cube
                self.x_2 -= self.side_cube
                self.x_3 -= self.side_cube
                self.x_4 -= self.side_cube
            if left_flag and self.position != 1:
                self.x_1 += self.side_cube
                self.x_2 += self.side_cube
                self.x_3 += self.side_cube
                self.x_4 += self.side_cube

    def turn_disable(self):
        self.left_flag = False
        self.right_flag = False
        for object_packed in OBJECTS:
            Checklist_x = [object_packed.x_1,object_packed.x_2,object_packed.x_3,object_packed.x_4]
            Checklist_y = [object_packed.y_1,object_packed.y_2,object_packed.y_3,object_packed.y_4]
            for cube in enumerate(Checklist_x):
                if self.position == 1:
                    if (Checklist_y[cube[0]] <= self.y_3 - self.side_cube < Checklist_y[cube[0]] + self.side_cube and
                    cube[1] == self.x_3):
                        return True
                elif self.position == 2:
                    if self.check_on_cube(self.x_4,self.y_4,cube[1],Checklist_y[cube[0]]):
                        self.right_flag = True
                    elif self.check_on_cube(-self.x_4,self.y_4,cube[1],Checklist_y[cube[0]]):
                        self.left_flag = True
                    if self.left_flag and self.right_flag:
                        return True
                elif self.position == 3:
                    if (
                        self.check_on_cube(-self.x_1,self.y_1-self.side_cube,cube[1],Checklist_y[cube[0]]) or
                        self.check_on_cube(-self.x_1,self.y_1,cube[1],Checklist_y[cube[0]])
                    ):
                        self.left_flag = True
                    elif self.check_on_cube(self.x_1,self.y_1,cube[1],Checklist_y[cube[0]]):
                        self.right_flag = True
                    if self.left_flag and self.right_flag:
                        return True
                elif self.position == 4:
                    if (
                        self.check_on_cube(self.x_1,self.y_1,cube[1],Checklist_y[cube[0]]) or
                        self.check_on_cube(self.x_2,self.y_2,cube[1],Checklist_y[cube[0]])
                    ):
                        self.right_flag = True
                    elif self.check_on_cube(-self.x_3,self.y_3,cube[1],Checklist_y[cube[0]]):
                        self.left_cube = True
                    if self.right_flag and self.left_flag:
                        return True
        return False


class L(Figures):

    def __init__(self, x, y, color):
        self.color = color
        self.side_cube = 30
        self.x_1 = x
        self.y_1 = y
        self.x_2 = x - self.side_cube
        self.y_2 = y
        self.x_3 = x - self.side_cube
        self.y_3 = y - self.side_cube
        self.x_4 = x - self.side_cube
        self.y_4 = y - 2*self.side_cube
        self.position = 1
        self.x_wait = self.draw_rect()[0] + WIDTH_RECT // 2
        self.y_wait = self.draw_rect()[1] + HEIGHT_RECT // 2 + self.side_cube // 2

    def turn(self):
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_SPACE and self.position == 1:
                self.x_1 -= self.side_cube
                self.y_2 -= self.side_cube
                self.x_3 += self.side_cube
                self.x_4 += 2*self.side_cube
                self.y_4 += self.side_cube
                self.position = 2
            elif event.key == pygame.K_SPACE and self.position == 2:
                self.y_1 -= 2*self.side_cube
                self.x_2 += self.side_cube
                self.y_2 -= self.side_cube
                self.x_4 -= self.side_cube
                self.y_4 += self.side_cube
                self.position = 3
            elif event.key == pygame.K_SPACE and self.position == 3:
                self.x_1 += 2*self.side_cube
                self.y_1 += self.side_cube
                self.x_2 += self.side_cube
                self.y_2 += 2*self.side_cube
                self.y_3 += self.side_cube
                self.x_4 -= self.side_cube
                self.position = 4
            elif event.key == pygame.K_SPACE and self.position == 4:
                self.x_1 -= self.side_cube
                self.y_1 += self.side_cube
                self.x_2 -= 2*self.side_cube
                self.x_3 -= self.side_cube
                self.y_3 -= self.side_cube
                self.y_4 -= 2*self.side_cube
                self.position = 1
            self.turn_adjustments(self.right_flag, event)

    def turn_adjustments(self, right_flag, event):
        if event.key == pygame.K_SPACE:
            shell = Shell()
            if (
                right_flag and self.position in [2, 4] or
                self.x_1 + 2*self.side_cube > shell.draw_line() or
                self.x_4 + 2*self.side_cube > shell.draw_line()
            ):
                self.x_1 -= self.side_cube
                self.x_2 -= self.side_cube
                self.x_3 -= self.side_cube
                self.x_4 -= self.side_cube

    def turn_disable(self):
        self.left_flag = False
        self.right_flag = False
        for object_packed in OBJECTS:
            Checklist_x = [object_packed.x_1, object_packed.x_2, object_packed.x_3, object_packed.x_4]
            Checklist_y = [object_packed.y_1, object_packed.y_2, object_packed.y_3, object_packed.y_4]
            for cube in enumerate(Checklist_x):
                if self.position == 1:
                    if self.check_on_cube(self.x_3, self.y_3, cube[1], Checklist_y[cube[0]]):
                        return True
                    if self.check_on_cube(self.x_1, self.y_1 - self.side_cube, cube[1], Checklist_y[cube[0]]):
                        self.right_flag = True
                    elif (
                        self.check_on_cube(-self.x_3, self.y_3, cube[1], Checklist_y[cube[0]]) and
                        self.check_on_cube(-self.x_2, self.y_2, cube[1], Checklist_y[cube[0]])
                    ):
                        self.left_flag = True
                    if self.left_flag and self.right_flag:
                        return True
                elif self.position == 2:
                    if (
                       (Checklist_y[cube[0]] <= self.y_2 - self.side_cube < Checklist_y[cube[0]] + self.side_cube and
                        cube[1] == self.x_2) or
                       (Checklist_y[cube[0]] <= self.y_3 - self.side_cube < Checklist_y[cube[0]] + self.side_cube and
                        cube[1] == self.x_3)
                       ):
                        return True
                elif self.position == 3:
                    if (
                        self.check_on_cube(self.x_3, self.y_3, cube[1], Checklist_y[cube[0]]) or
                        self.check_on_cube(self.x_4, self.y_4, cube[1], Checklist_y[cube[0]])
                       ):
                        self.right_flag = True
                    elif (
                        self.check_on_cube(-self.x_4, self.y_4, cube[1], Checklist_y[cube[0]]) or
                        self.check_on_cube(-(self.x_4 - self.side_cube), self.y_4, cube[1], Checklist_y[cube[0]])
                         ):
                        self.left_flag = True
                    if self.left_flag and self.right_flag:
                        return True
                elif self.position == 4:
                    if (
                       (Checklist_y[cube[0]] <= self.y_4 - self.side_cube < Checklist_y[cube[0]] + self.side_cube and
                        cube[1] == self.x_4) or
                       (Checklist_y[cube[0]] <= self.y_4 - 2*self.side_cube < Checklist_y[cube[0]] + self.side_cube and
                        cube[1] == self.x_4)
                       ):
                        return True
        return False
        

class O(Figures):

    def __init__(self, x, y, color):
        self.color = color
        self.side_cube = 30
        self.x_1 = x
        self.y_1 = y
        self.x_2 = x - self.side_cube
        self.y_2 = y
        self.x_3 = x - self.side_cube
        self.y_3 = y - self.side_cube
        self.x_4 = x
        self.y_4 = y - self.side_cube
        self.x_wait = self.draw_rect()[0] + WIDTH_RECT // 2
        self.y_wait = self.draw_rect()[1] + HEIGHT_RECT // 2


class GameTools():

    def __init__(self):
        self.font = FONT
        self.font.set_bold(True)
        self.time = 0
        self.fps = round(CLOCK.get_fps())
        self.score = 0
        self.pause = True
        self.black = (0, 0, 0)
        self.score_table = (self.font.render('Time: {}'.format(self.time // 1000), True, self.black),
                            self.font.render('FPS: {}'.format(self.fps), True, self.black),
                            self.font.render('Score: {}'.format(self.score), True, self.black))
        self.control_table = (self.font.render('Turn: SPACE', True, self.black),
                              self.font.render('Pause: ENTER', True, self.black))
        self.game_over_table = (self.font.render('GAME OVER', True, self.black),
                                self.font.render('Your Score: {}'.format(self.score), True, self.black),
                                self.font.render('Press ENTER to start a new game', True, self.black),
                                self.font.render('Press ESC to exit', True, self.black))
        self.paused_table = (self.font.render('GAME IS PAUSED', True, self.black),
                             self.font.render('Press ENTER to unpause', True, self.black))

    def blit_table(self, pos: tuple, table):
        x, y = pos
        for line_surface in table:
            SCREEN.blit(line_surface, (x, y))
            height_line = line_surface.get_height()
            y += height_line

    def game_over_check(self, checklist):
        for y in checklist:
            if y < 0:
                return True
        return False

    def game_stop(self, table):
        while self.pause:
            CLOCK.tick(20)
            raw_height = table[0].get_height()
            raw_width = table[0].get_width()
            x, y = (WIDTH // 2 - raw_width // 2, HEIGHT // 2 - raw_height)
            for line in table:
                SCREEN.blit(line, (x, y))
                y += line.get_height()
            pygame.display.update()
            for event in pygame.event.get(eventtype=pygame.KEYUP):
                if event.key == pygame.K_RETURN:
                    return False
                if event.key == pygame.K_ESCAPE:
                    return True


pygame.init()

WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
X_LINE, Y_LINE = (680, 0)
LEFT_RECT, TOP_RECT = (700, 200)
WIDTH_RECT, HEIGHT_RECT = (240, 130)
RECT_BORDER_RADIUS = 4
RUN_GAME = True
CLOCK = pygame.time.Clock()
OBJECTS = []
FONT = pygame.font.Font("assets/Font/tahoma.ttf", 24)


Game = GameTools()

objec = I(310, -4, (40, 25, 77))
objec_wait = Z(310, -4, (174, 122, 14))


while RUN_GAME:
    SCREEN.fill((255, 255, 255))

    Game.time += CLOCK.tick(20)
    Game.fps = round(CLOCK.get_fps())
    Game.score_table = (Game.font.render('Time: {}'.format(Game.time // 1000), True, Game.black),
                        Game.font.render('FPS: {}'.format(Game.fps), True, Game.black),
                        Game.font.render('Score: {}'.format(Game.score), True, Game.black))
    Game.blit_table((740, 800), Game.score_table)
    Game.blit_table((740, 500), Game.control_table)
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
            Game.blit_table((740, 800), Game.score_table)
            pygame.display.update()
            pygame.time.wait(2000)
            Game.score += 10
        OBJECTS.append(objec)
        objec = objec_wait
        objec_wait = random.choice([Z(310, -4, (174, 122, 14)),
                                    I(310, -4, (40, 25, 77)),
                                    J(310, -4, (0, 128, 0)),
                                    S(310, -4, (43, 52, 65)),
                                    T(310, -4, (220, 20, 60)),
                                    L(310, -4, (255, 165, 0)),
                                    O(310, -4, (135, 206, 235))])
        objec.act()
        objec_wait.wait()

    for objec_packed in OBJECTS:
        objec_packed.show()

    for event in pygame.event.get(eventtype=pygame.KEYUP):
        if event.key == pygame.K_RETURN:
            Game.game_stop(Game.paused_table)
    
    if pygame.event.peek(pygame.QUIT):
        RUN_GAME = False


    pygame.display.update()

    try:
        object_check_go = OBJECTS[-1]
        if Game.game_over_check([object_check_go.y_1, object_check_go.y_2, object_check_go.y_3, object_check_go.y_4]):
            SCREEN.fill((255, 255, 255))
            Game.game_over_table = (Game.font.render('GAME OVER', True, Game.black),
                                    Game.font.render('Your Score: {}'.format(Game.score), True, Game.black),
                                    Game.font.render('Press ENTER to start a new game', True, Game.black),
                                    Game.font.render('Press ESC to exit', True, Game.black))
            if Game.game_stop(Game.game_over_table):
                RUN_GAME = False
            else:
                OBJECTS.clear()
                Game.score = Game.time = 0
    except IndexError:
        pass
    

pygame.quit()
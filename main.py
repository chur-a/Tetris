import random
import pygame
from game_tools import GameTools


class Figures:
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
        object_w = self.__class__(self.x_wait, self.y_wait, self.color)
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
            for check_x, check_y in zip(Checklist_x, Checklist_y):
                if (
                        self.check_on_cube(self.x_2, self.y_2, check_x, check_y) or
                        self.check_on_cube(self.x_1, self.y_1, check_x, check_y) or
                        self.check_on_cube(self.x_3, self.y_3, check_x, check_y) or
                        self.check_on_cube(self.x_4, self.y_4, check_x, check_y)
                ):
                    self.right_boarder = True
                if (
                        self.check_on_cube(-self.x_2, self.y_2, check_x, check_y) or
                        self.check_on_cube(-self.x_1, self.y_1, check_x, check_y) or
                        self.check_on_cube(-self.x_3, self.y_3, check_x, check_y) or
                        self.check_on_cube(-self.x_4, self.y_4, check_x, check_y)
                ):
                    self.left_boarder = True

    def check_collision_borders(self):
        for x in [self.x_1, self.x_2, self.x_3, self.x_4]:
            if x <= self.side_cube:
                self.left_boarder = True
                break
            elif x + self.side_cube >= X_LINE - self.side_cube:
                self.right_boarder = True
                break

    def equalization(self, level, cube_level):
        diff = cube_level + self.side_cube - level
        self.y_1 -= diff
        self.y_2 -= diff
        self.y_3 -= diff
        self.y_4 -= diff

    def raw(self):
        Y = [('self1', self.y_1), ('self2', self.y_2), ('self3', self.y_3), ('self4', self.y_4)]
        Raws = [[] for _ in range(4)]
        for y in Y:
            for raw in Raws:
                if not raw or y[1] == raw[0][1]:
                    raw.append(y)
                    break

        for object_packed in enumerate(OBJECTS):
            Checklist_y = [object_packed[1].y_1, object_packed[1].y_2, object_packed[1].y_3, object_packed[1].y_4]
            for i in range(len(Checklist_y)):
                for raw in Raws:
                    if raw and Checklist_y[i] == raw[0][1]:
                        raw.append((object_packed[0], i))
                        break

        for rawlist in sorted((raw for raw in Raws if raw), key=lambda item: item[0][1]):
            if len(rawlist) == 22:
                self.raw_equalization(rawlist[0][1])
                self.raw_rect(rawlist[0][1])
                self.raw_eliminate(rawlist)
                self.raw_show()
                Game.score += 10

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
        objec_wait.wait()
        Game.game_update()
        Game.sounds['BackgroundMusic'].set_volume(0.5)
        Game.sounds['RawMusic'].play()
        pygame.display.update()
        pygame.time.wait(2000)
        Game.sounds['BackgroundMusic'].set_volume(1)


class Z(Figures):
    def __init__(self, x, y, color):
        self.color = color
        self.x_1 = x
        self.y_1 = y
        self.side_cube = CUBE_SIZE
        self.x_2 = x + self.side_cube
        self.y_2 = y
        self.x_3 = x + self.side_cube
        self.y_3 = y + self.side_cube
        self.x_4 = x + 2*self.side_cube
        self.y_4 = y + self.side_cube
        self.position = 1
        self.left_boarder = False
        self.right_boarder = False
        self.x_wait = LEFT_RECT + WIDTH_RECT//2 - 1.5*self.side_cube
        self.y_wait = TOP_RECT + HEIGHT_RECT//2 - self.side_cube

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
            self.turn_adjustment(self.right_flag, event)

    def turn_adjustment(self, right_flag, event):
        if event.key == pygame.K_SPACE:
            if right_flag or self.x_4 + self.side_cube > X_LINE:
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
            if self.position == 1:
                for check_x, check_y in zip(Checklist_x, Checklist_y):
                    if check_y <= self.y_2 - self.side_cube < check_y + self.side_cube and check_x == self.x_2:
                        return True
            elif self.position == 0:
                for check_x, check_y in zip(Checklist_x, Checklist_y):
                    if self.check_on_cube(self.x_4 + self.side_cube, self.y_4, check_x, check_y):
                        self.right_flag = True
                    elif self.check_on_cube(-self.x_3, self.y_3, check_x, check_y):
                        self.left_flag = True
                    if (
                        (self.left_flag and self.right_flag) or
                        self.check_on_cube(self.x_4, self.y_4, check_x, check_y)
                    ):
                        return True
        return False
        

class I(Figures):
    def __init__(self, x, y, color):
        self.x_1 = x
        self.y_1 = y
        self.side_cube = CUBE_SIZE
        self.y_2 = self.y_1 + self.side_cube
        self.y_3 = self.y_2 + self.side_cube
        self.y_4 = self.y_3 + self.side_cube
        self.x_2 = self.x_3 = self.x_4 = self.x_1
        self.position = 1
        self.color = color
        self.left_boarder = False
        self.right_boarder = False
        self.x_wait = LEFT_RECT + WIDTH_RECT//2 - self.side_cube//2
        self.y_wait = TOP_RECT + HEIGHT_RECT//2 - 2*self.side_cube
        
    def turn_disable(self):
        self.left_flag_sm = self.right_flag_sm = False
        self.left_flag_bg = self.right_flag_bg = False
        self.left_flag_lf = self.right_flag_lf = False
        for object_packed in OBJECTS:
            Checklist_x = [object_packed.x_1, object_packed.x_2, object_packed.x_3, object_packed.x_4]
            Checklist_y = [object_packed.y_1, object_packed.y_2, object_packed.y_3, object_packed.y_4]
            if self.position == 1:
                for check_x, check_y in zip(Checklist_x, Checklist_y):
                    if self.y_2 - self.side_cube <= check_y <= self.y_2 + self.side_cube:
                        if self.check_on_cube(self.x_2 + self.side_cube, self.y_2, check_x, check_y):
                            self.right_flag_bg = True
                        elif self.check_on_cube(-(self.x_2 - self.side_cube), self.y_2, check_x, check_y):
                            self.left_flag_bg = True
                        elif self.check_on_cube(self.x_2, self.y_2, check_x, check_y):
                            self.right_flag_sm = True
                        elif self.check_on_cube(-(self.x_2 - 2*self.side_cube), self.y_2, check_x, check_y):
                            self.left_flag_sm = True
                        elif self.check_on_cube(-self.x_2, self.y_2, check_x, check_y):
                            self.left_flag_lf = True
                        elif self.check_on_cube(self.x_2 + 2*self.side_cube, self.y_2, check_x, check_y):
                            self.right_flag_lf = True
                        if (
                                (self.left_flag_bg and self.right_flag_bg) or
                                (self.left_flag_sm and self.right_flag_sm) or
                                (self.left_flag_lf and self.right_flag_lf)
                        ):
                            return True
            elif self.position == 0:
                for check_x, check_y in zip(Checklist_x, Checklist_y):
                    if (
                        (
                         (
                            (self.x_2 == check_x and not self.left_boarder) or
                            (self.x_1 == check_x and self.left_boarder) or
                            (self.x_4 == check_x and self.right_boarder)
                         ) and
                         (
                            check_y <= self.y_2 - self.side_cube <= check_y + self.side_cube
                            or
                            check_y <= self.y_2 + self.side_cube <= check_y + self.side_cube
                            or
                            check_y <= self.y_2 + 2*self.side_cube <= check_y + self.side_cube
                         )
                        ) or
                            self.y_2 + 3*self.side_cube > HEIGHT
                    ):
                        return True
        return False
    
    def turn(self):
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_SPACE and self.position == 1:
                self.y_1 = self.y_3 = self.y_4 = self.y_2
                self.x_1 -= self.side_cube
                self.x_3 += self.side_cube
                self.x_4 += 2*self.side_cube
                self.position = 0
            elif event.key == pygame.K_SPACE and self.position == 0:
                self.x_1 = self.x_3 = self.x_4 = self.x_2
                self.y_1 -= self.side_cube
                self.y_3 += self.side_cube
                self.y_4 += 2*self.side_cube
                self.position = 1
            self.turn_adjustment(event)

    def turn_adjustment(self, event):
        if event.key == pygame.K_SPACE:
            if (
                    (self.right_flag_sm and not self.left_flag_sm) or
                    self.x_4 + self.side_cube > X_LINE
            ):
                self.x_1 -= 2*self.side_cube
                self.x_2 -= 2*self.side_cube
                self.x_3 -= 2*self.side_cube
                self.x_4 -= 2*self.side_cube
            elif self.right_flag_bg and not self.left_flag_bg:
                self.x_1 -= self.side_cube
                self.x_2 -= self.side_cube
                self.x_3 -= self.side_cube
                self.x_4 -= self.side_cube
            if (
                    (self.left_flag_lf and not self.right_flag_lf) or
                    self.x_1 - self.side_cube < 0
            ):
                self.x_1 += self.side_cube
                self.x_2 += self.side_cube
                self.x_3 += self.side_cube
                self.x_4 += self.side_cube


class J(Figures):
    def __init__(self, x, y, color):
        self.color = color
        self.x_1 = x
        self.y_1 = y
        self.side_cube = CUBE_SIZE
        self.x_2 = self.x_1
        self.y_2 = self.y_1 + self.side_cube
        self.x_3 = self.x_2 + self.side_cube
        self.y_3 = self.y_2
        self.x_4 = self.x_3 + self.side_cube
        self.y_4 = self.y_3
        self.position = 1
        self.x_wait = LEFT_RECT + WIDTH_RECT//2 - 3*self.side_cube//2
        self.y_wait = TOP_RECT + HEIGHT_RECT//2 - self.side_cube
            
    def turn_disable(self):
        self.left_flag = False
        self.right_flag = False
        for object_packed in OBJECTS:
            Checklist_x =[object_packed.x_1, object_packed.x_2, object_packed.x_3, object_packed.x_4]
            Checklist_y =[object_packed.y_1, object_packed.y_2, object_packed.y_3, object_packed.y_4]
            for check_x, check_y in zip(Checklist_x, Checklist_y):
                if self.position == 1:
                    if (
                        self.check_on_cube(self.x_1, self.y_1, check_x, check_y) or
                        self.check_on_cube(self.x_1, self.y_1 - self.side_cube, check_x, check_y) or
                        self.check_on_cube(self.x_3, self.y_3 - 2*self.side_cube, check_x, check_y)
                    ):
                        return True
                elif self.position == 2:
                    if (
                        self.check_on_cube(self.x_3 + self.side_cube, self.y_3, check_x, check_y) or
                        self.check_on_cube(self.x_4 + self.side_cube, self.y_4, check_x, check_y)
                    ):
                        self.right_flag = True
                    elif self.check_on_cube(-self.x_3, self.y_3, check_x, check_y):
                        self.left_flag = True
                    if (
                        (self.right_flag and self.left_flag) or
                        self.check_on_cube(self.x_3, self.y_3, check_x, check_y)
                    ):
                        return True
                elif self.position == 3:
                    if (
                        self.check_on_cube(-self.x_1, self.y_1, check_x, check_y) or
                        self.check_on_cube(-(self.x_1 - self.side_cube), self.y_1, check_x, check_y) or
                        self.check_on_cube(-self.x_2, self.y_2 - self.side_cube, check_x, check_y)
                    ):
                        return True
                elif self.position == 4:
                    if self.check_on_cube(self.x_2, self.y_2, check_x, check_y):
                        self.right_flag = True
                    elif (
                          self.check_on_cube(-self.x_1, self.y_1, check_x, check_y) or
                          self.check_on_cube(-self.x_1, self.y_1 - self.side_cube, check_x, check_y)
                    ):
                        self.left_flag = True
                    if (
                        (self.left_flag and self.right_flag) or
                        self.check_on_cube(-self.x_3, self.y_3, check_x, check_y)
                    ):
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
            self.turn_adjustment(self.right_flag, event)

    def turn_adjustment(self, right_flag, event):
        if event.key == pygame.K_SPACE:
            if right_flag or self.x_3 + 2*self.side_cube > X_LINE:
                self.x_1 -= self.side_cube
                self.x_2 -= self.side_cube
                self.x_3 -= self.side_cube
                self.x_4 -= self.side_cube


class S(Figures):
    def __init__(self, x, y, color):
        self.color = color
        self.x_1 = x
        self.y_1 = y
        self.side_cube = CUBE_SIZE
        self.x_2 = x - self.side_cube
        self.y_2 = y
        self.x_3 = x - self.side_cube
        self.y_3 = y + self.side_cube
        self.x_4 = x - 2*self.side_cube
        self.y_4 = y + self.side_cube
        self.position = 1
        self.x_wait = LEFT_RECT + WIDTH_RECT // 2 + self.side_cube // 2
        self.y_wait = TOP_RECT + HEIGHT_RECT // 2 - self.side_cube
            
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
        if right_flag or self.x_1 + self.side_cube > X_LINE:
            self.x_1 -= self.side_cube
            self.x_2 -= self.side_cube
            self.x_3 -= self.side_cube
            self.x_4 -= self.side_cube

    def turn_disable(self):
        self.left_flag = False
        self.right_flag = False
        for object_packed in OBJECTS:
            Checklist_x =[object_packed.x_1, object_packed.x_2, object_packed.x_3, object_packed.x_4]
            Checklist_y =[object_packed.y_1, object_packed.y_2, object_packed.y_3, object_packed.y_4]
            if self.position == 1:
                for check_x, check_y in zip(Checklist_x, Checklist_y):
                    if (
                            check_y <= self.y_2 - self.side_cube < check_y + self.side_cube and
                            check_x == self.x_2 - self.side_cube
                    ):
                         return True
            elif self.position == 0:
                for check_x, check_y in zip(Checklist_x, Checklist_y):
                    if self.check_on_cube(-self.x_4, self.y_4, check_x, check_y):
                        return True
                    if self.check_on_cube(self.x_3, self.y_3, check_x, check_y):
                        self.right_flag = True
                    elif self.check_on_cube(-(self.x_4 - self.side_cube), self.y_4, check_x, check_y):
                        self.left_flag = True
                    if self.left_flag and self.right_flag:
                        return True
        return False


class T(Figures):

    def __init__(self, x, y, color):
        self.color = color
        self.side_cube = CUBE_SIZE
        self.x_1 = x
        self.y_1 = y
        self.x_2 = x - self.side_cube
        self.y_2 = y - self.side_cube
        self.x_3 = x
        self.y_3 = y - self.side_cube
        self.x_4 = x + self.side_cube
        self.y_4 = y - self.side_cube
        self.position = 1
        self.x_wait = LEFT_RECT + WIDTH_RECT // 2 - self.side_cube // 2
        self.y_wait = TOP_RECT + HEIGHT_RECT // 2

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
            self.turn_adjustment(self.right_flag, event)

    def turn_adjustment(self, right_flag, event):
        if event.key == pygame.K_SPACE:
            if right_flag or self.x_1 + 2*self.side_cube > X_LINE:
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
            for check_x, check_y in zip(Checklist_x, Checklist_y):
                if self.position == 1:
                    if check_y <= self.y_3 - self.side_cube < check_y + self.side_cube and check_x == self.x_3:
                        return True
                elif self.position == 2:
                    if self.check_on_cube(self.x_4, self.y_4, check_x, check_y):
                        self.right_flag = True
                    elif self.check_on_cube(-(self.x_4-self.side_cube), self.y_4, check_x, check_y):
                        self.left_flag = True
                    if (
                        (self.left_flag and self.right_flag) or
                        self.check_on_cube(-self.x_4, self.y_4, check_x, check_y)
                    ):
                        return True
                elif self.position == 3:
                    if (
                        self.check_on_cube(-self.x_1, self.y_1-self.side_cube, check_x, check_y) or
                        self.check_on_cube(-self.x_1, self.y_1, check_x, check_y)
                    ):
                        return True
                elif self.position == 4:
                    if (
                        self.check_on_cube(self.x_1, self.y_1, check_x, check_y) or
                        self.check_on_cube(self.x_2, self.y_2, check_x, check_y)
                    ):
                        self.right_flag = True
                    elif self.check_on_cube(-self.x_3, self.y_3, check_x, check_y):
                        self.left_cube = True
                    if self.right_flag and self.left_flag:
                        return True
        return False


class L(Figures):

    def __init__(self, x, y, color):
        self.color = color
        self.side_cube = CUBE_SIZE
        self.x_1 = x
        self.y_1 = y
        self.x_2 = x - self.side_cube
        self.y_2 = y
        self.x_3 = x - self.side_cube
        self.y_3 = y - self.side_cube
        self.x_4 = x - self.side_cube
        self.y_4 = y - 2*self.side_cube
        self.position = 1
        self.x_wait = LEFT_RECT + WIDTH_RECT // 2
        self.y_wait = TOP_RECT + HEIGHT_RECT // 2 + self.side_cube // 2

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
            self.turn_adjustment(self.right_flag, event)

    def turn_adjustment(self, right_flag, event):
        if event.key == pygame.K_SPACE:
            if (
                right_flag or
                self.x_1 + 2*self.side_cube > X_LINE or
                self.x_4 + 2*self.side_cube > X_LINE
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
            for check_x, check_y in zip(Checklist_x, Checklist_y):
                if self.position == 1:
                    if self.check_on_cube(self.x_3, self.y_3, check_x, check_x):
                        return True
                    if self.check_on_cube(self.x_1, self.y_1 - self.side_cube, check_x, check_x):
                        self.right_flag = True
                    elif (
                        self.check_on_cube(-self.x_3, self.y_3, check_x, check_y) and
                        self.check_on_cube(-self.x_2, self.y_2, check_x, check_y)
                    ):
                        self.left_flag = True
                    if self.left_flag and self.right_flag:
                        return True
                elif self.position == 2:
                    if (
                        (check_y <= self.y_2 - self.side_cube < check_y + self.side_cube and check_x == self.x_2) or
                        (check_y <= self.y_3 - self.side_cube < check_y + self.side_cube and check_x == self.x_3)
                       ):
                        return True
                elif self.position == 3:
                    if (
                        self.check_on_cube(self.x_3, self.y_3, check_x, check_y) or
                        self.check_on_cube(self.x_4, self.y_4, check_x, check_y)
                       ):
                        self.right_flag = True
                    elif self.check_on_cube(-self.x_4, self.y_4, check_x, check_y):
                        self.left_flag = True
                    if (
                            (self.left_flag and self.right_flag) or
                            self.check_on_cube(-(self.x_4 - self.side_cube), self.y_4, check_x, check_y)
                    ):
                        return True
                elif self.position == 4:
                    if (
                       (check_y <= self.y_4 - self.side_cube < check_y + self.side_cube and check_x == self.x_4) or
                       (check_y <= self.y_4 - 2*self.side_cube < check_y + self.side_cube and check_x == self.x_4)
                       ):
                        return True
        return False
        

class O(Figures):

    def __init__(self, x, y, color):
        self.color = color
        self.side_cube = CUBE_SIZE
        self.x_1 = x
        self.y_1 = y
        self.x_2 = x - self.side_cube
        self.y_2 = y
        self.x_3 = x - self.side_cube
        self.y_3 = y - self.side_cube
        self.x_4 = x
        self.y_4 = y - self.side_cube
        self.x_wait = LEFT_RECT + WIDTH_RECT // 2
        self.y_wait = TOP_RECT + HEIGHT_RECT // 2

    def turn_disable(self):
        return True


pygame.init()

WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
X_LINE, Y_LINE = (680, 0)
LEFT_RECT, TOP_RECT = (700, 200)
WIDTH_RECT, HEIGHT_RECT = (240, 130)
CUBE_SIZE = 30
RUN_GAME = True
CLOCK = pygame.time.Clock()
OBJECTS = []
FONT = pygame.font.Font("assets/Font/tahoma.ttf", 24)


Game = GameTools(FONT, CLOCK, WIDTH, HEIGHT, SCREEN, (X_LINE, Y_LINE), (LEFT_RECT, TOP_RECT, WIDTH_RECT, HEIGHT_RECT))

Game.sounds['BackgroundMusic'].play(loops=-1)
pygame.display.set_caption('Tetris')

objec = I(310, -4, (40, 25, 77))
objec_wait = Z(310, -4, (174, 122, 14))


while RUN_GAME:
    SCREEN.fill((255, 255, 255))
    Game.game_update()
    pygame.event.pump()

    if not objec.stop():
        objec.act()
        objec_wait.wait()
    else:
        objec.raw()
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

    for event in pygame.event.get(eventtype=(pygame.KEYUP, pygame.QUIT)):
        if Game.event_handler(event) == 'QUIT':
            RUN_GAME = False
        elif Game.event_handler(event) == 'RETURN':
            if Game.game_stop(Game.paused_table):
                RUN_GAME = False

    pygame.display.update()

    try:
        object_check_go = OBJECTS[-1]
        if Game.game_over_check([object_check_go.y_1, object_check_go.y_2, object_check_go.y_3, object_check_go.y_4]):
            if Game.game_over():
                RUN_GAME = False
            else:
                Game.game_restart()
                OBJECTS.clear()
    except IndexError:
        pass


pygame.quit()

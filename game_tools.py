import pygame


class GameTools:

    def __init__(self, font, clock, width, height, screen, line, rect):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.font.set_bold(True)
        self.width, self.height = width, height
        self.x_line, self.y_line = line
        self.left_rect, self.top_rect, self.width_rect, self.height_rect = rect
        self.time = self.score = 0
        self.fps = round(clock.get_fps())
        self.black = (0, 0, 0)
        self.control_table = (self.font.render('Turn: SPACE', True, self.black),
                              self.font.render('Pause: ENTER', True, self.black),
                              self.font.render('Exit: ESC', True, self.black))
        self.paused_table = (self.font.render('GAME IS PAUSED', True, self.black),
                             self.font.render('Press ENTER to unpause', True, self.black),
                             self.font.render('Press ESC to exit', True, self.black))
        self.sounds = {'BackgroundMusic': pygame.mixer.Sound("assets/Sounds/Tetris_theme.mp3"),
                       'RawMusic': pygame.mixer.Sound("assets/Sounds/raw.mp3"),
                       'GameOver': pygame.mixer.Sound("assets/Sounds/Game_over.mp3")}

    @property
    def score_table(self):
        return (self.font.render('Time: {}'.format(self.time // 1000), True, self.black),
                self.font.render('FPS: {}'.format(self.fps), True, self.black),
                self.font.render('Score: {}'.format(self.score), True, self.black))

    @property
    def game_over_table(self):
        return (self.font.render('GAME OVER', True, self.black),
                self.font.render('Your Score: {}'.format(self.score), True, self.black),
                self.font.render('Press ENTER to start a new game', True, self.black),
                self.font.render('Press ESC to exit', True, self.black))

    def draw_lines(self):
        pygame.draw.line(self.screen, (0, 0, 255), (self.x_line, self.y_line),
                         (self.x_line, self.y_line + self.height), 5)
        pygame.draw.rect(self.screen, (255, 0, 255),
                         (self.left_rect, self.top_rect, self.width_rect, self.height_rect),
                         width=5, border_radius=4)

    def blit_table(self, pos: tuple, table):
        x, y = pos
        for line_surface in table:
            self.screen.blit(line_surface, (x, y))
            height_line = line_surface.get_height()
            y += height_line

    def game_update(self):
        self.draw_lines()
        self.time += self.clock.tick(20)
        self.fps = round(self.clock.get_fps())
        self.blit_table((740, 800), self.score_table)
        self.blit_table((740, 500), self.control_table)

    def game_over_check(self, checklist):
        for y in checklist:
            if y < 0:
                return True
        return False

    def game_stop(self, table):
        while True:
            self.clock.tick(20)
            raw_height = table[0].get_height()
            raw_width = table[0].get_width()
            x, y = (self.width // 2 - raw_width // 2 - 50, self.height // 2 - raw_height)
            for line in table:
                self.screen.blit(line, (x, y))
                y += line.get_height()
            pygame.display.update()
            for event in pygame.event.get(eventtype=(pygame.KEYUP, pygame.QUIT)):
                if self.event_handler(event) == 'QUIT':
                    return True
                elif self.event_handler(event) == 'RETURN':
                    return False

    def event_handler(self, event):
        if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE:
            return 'QUIT'
        elif event.key == pygame.K_RETURN:
            return 'RETURN'


    def game_over(self):
        self.screen.fill((255, 255, 255))
        pygame.mixer.stop()
        self.sounds['GameOver'].play(loops=-1)
        if self.game_stop(self.game_over_table):
            return True
        else:
            return False

    def game_restart(self):
        self.sounds['GameOver'].stop()
        self.sounds['BackgroundMusic'].play(loops=-1)
        self.score = self.time = 0

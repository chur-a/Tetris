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
        self.green = (124, 252, 0)
        self.yellow = (255, 255, 0)
        self.button = None
        self.event_status = None
        self.control_table = (self.font.render('Turn: SPACE', True, self.black),
                              self.font.render('Pause: ENTER', True, self.black),
                              self.font.render('Exit: ESC', True, self.black))
        self.paused_table = ('GAME ON PAUSE', 'RESUME', 'SETTINGS', 'EXIT')
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
        return f'GAME OVER, YOUR SCORE: {self.score}', 'NEW GAME', 'SETTINGS', 'EXIT'

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
        self.event_status = None
        self.draw_lines()
        self.time += self.clock.tick(20)
        self.fps = round(self.clock.get_fps())
        self.blit_table((740, 800), self.score_table)
        self.blit_table((740, 500), self.control_table)
        self.event_handler()

    def game_over_check(self, checklist):
        for y in checklist:
            if y < 0:
                return True
        return False

    def draw_menu(self, title, table):
        x_menu, y_menu = self.width//2 - 150, 200
        x_mouse, y_mouse = pygame.mouse.get_pos()
        title = self.font.render(title, True, self.black)
        self.screen.blit(title, (x_menu + 150 - title.get_width()//2, y_menu - 60))
        for button_text in table:
            if x_menu <= x_mouse <= x_menu + 330 and y_menu <= y_mouse <= y_menu + 130:
                pygame.draw.rect(self.screen, self.yellow, (x_menu - 30, y_menu - 30, 360, 160))
                pygame.draw.rect(self.screen, self.green, (x_menu - 10, y_menu - 10, 320, 120))
                self.button = button_text
            else:
                pygame.draw.rect(self.screen, self.yellow, (x_menu - 15, y_menu - 15, 330, 130))
                pygame.draw.rect(self.screen, self.green, (x_menu, y_menu, 300, 100))
            button_text = self.font.render(button_text, True, self.black)
            x_text, y_text = x_menu + 150 - button_text.get_width()//2, y_menu + 50 - button_text.get_height()//2
            self.screen.blit(button_text, (x_text, y_text))
            y_menu += 150

    def event_handler(self):
        for event in pygame.event.get(eventtype=(pygame.KEYUP, pygame.QUIT, pygame.MOUSEBUTTONUP)):
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                self.event_status = 'QUIT'
                return
            elif event.type == pygame.KEYUP and event.key == 13:
                self.event_status = 'RETURN'
                return
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.button == 'RESUME':
                    self.button = None
                    self.event_status = 'RESUME'
                    return
                elif self.button == 'EXIT':
                    self.button = None
                    self.event_status = 'QUIT'
                    return
                elif self.button == 'NEW GAME':
                    self.button = None
                    self.event_status = 'NEW GAME'
                    return

    def game_stop(self, table):
        title = table[0]
        table = table[1:]
        self.event_status = None
        while True:
            self.clock.tick(20)
            self.screen.fill((255, 255, 255))
            self.draw_menu(title, table)
            pygame.display.update()
            self.event_handler()
            if self.event_status:
                return

    def game_over(self):
        pygame.mixer.stop()
        self.sounds['GameOver'].play(loops=-1)
        self.game_stop(self.game_over_table)
        if self.event_status == 'QUIT':
            return True
        elif self.event_status == 'NEW GAME':
            return False

    def game_restart(self):
        self.sounds['GameOver'].stop()
        self.sounds['BackgroundMusic'].play(loops=-1)
        self.score = self.time = 0

import pygame
import sys
import sqlite3
import ctypes
import random 

pygame.init()


class StartScreen:
    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (102, 186, 168)
        self.RED = (229, 0, 95)
        self.BLUE = (0, 0, 150)

        self.FPS = 50
        self.clock = pygame.time.Clock()
        self.start_screen()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Космический доставщик пиццы")

        fon = pygame.transform.scale(pygame.image.load('img/kosmos-77.webp'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        font = pygame.font.Font(None, 50)
        text = font.render("КОСМИЧЕСКИЙ ДОСТАВЩИК ПИЦЦЫ", True, self.WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, 200))
        screen.blit(text, text_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            flag = self.init_db()
            if flag:
                self.draw_button(screen, "Начать", 300, 300, 200, 50, self.BLUE, self.GREEN, lambda: self.start_screen_2())
            else:
                self.draw_button(screen, "Продолжить", 150, 350, 200, 50, self.BLUE, self.GREEN, lambda: self.start_game3())
                self.draw_button(screen, "Начать сначала", 450, 350, 200, 50, self.BLUE, self.RED, lambda: self.get_out())

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def init_db(self):
        con = sqlite3.connect('kosmicheskiy_dostavshchik_pitstsy.db')
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM player")
        result = cur.fetchone()[0]
        con.close()
        if result == 0:
            flag = True
            return flag
        else:
            flag = False
            return flag
        
    def draw_button(self, screen, text, x, y, width, height, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            pygame.draw.rect(screen, hover_color, (x, y, width, height))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, color, (x, y, width, height))

        font = pygame.font.Font(None, 30)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surface, text_rect)

    def get_out(self):
        con = sqlite3.connect('kosmicheskiy_dostavshchik_pitstsy.db')
        cur = con.cursor()
        cur.execute('DELETE FROM player')
        con.commit()
        self.start_screen()

    def start_screen_2(self):
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Описание игры")

        intro_text = ["Вы — космический доставщик пиццы, который должен",
                      "доставлять заказы на разные планеты.",
                      "Однако путь к каждой планете лежит через опасные",
                      "космические лабиринты, наполненные черными дырами",
                      "и метеоритами.",
                      "Ваша задача — пройти лабиринт, избегая препятствий,",
                      "и доставить пиццу вовремя."]
    
        fon = pygame.transform.scale(pygame.image.load('img/kosmos-77.webp'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        font = pygame.font.Font(None, 40)
        text1 = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(self.WHITE))
            intro_rect = string_rendered.get_rect()
            text1 += 10
            intro_rect.top = text1
            intro_rect.x = 10
            text1 += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
            self.draw_button(screen, "Продолжить", 300, 400, 200, 50, self.BLUE, self.GREEN, lambda: self.start_game3())
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def start_game3(self):
        gs = GameScreen()
        gs.run()


class GameScreen:
    def __init__(self):
        self.FPS = 50
        self.clock = pygame.time.Clock()

        self.WIDTH, self.HEIGHT = 1500, 700
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Космический доставщик пиццы")

        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetWindowPos(hwnd, 0, 10, 50, 0, 0, 0x0001)

        self.fon = pygame.transform.scale(pygame.image.load('img/kosmos-77.webp'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(self.fon, (0, 0))

        self.cell_size = 100
        self.grid_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        for row in range(7):
            for col in range(15):
                x = col * self.cell_size
                y = row * self.cell_size
                pygame.draw.rect(
                    self.grid_surface,
                    (255, 255, 255),
                    (x, y, self.cell_size, self.cell_size),
                    1
                )
        self.screen.blit(self.grid_surface, (0, 0))

        self.target_cell_x = 14
        self.target_cell_y = 0
        self.target_rect = pygame.Rect(
            self.target_cell_x * self.cell_size,
            self.target_cell_y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(self.screen, (102, 186, 168), self.target_rect)

        self.time_left = 25
        self.font = pygame.font.Font(None, 74)
        self.timer_rect = pygame.Rect(10, 10, 250, 50)

        con = sqlite3.connect('kosmicheskiy_dostavshchik_pitstsy.db')
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM player")
        result = cur.fetchone()[0]

        if result == 0:
            cur.execute("INSERT INTO player (level, points) VALUES (1, 0)")
            con.commit()

        cur.execute("SELECT level FROM player")
        result = cur.fetchone()

        if result[0] == 1:
            self.maze1 = self.level_1()
        elif result[0] == 2:
            self.maze1 = self.level_2()
        elif result[0] == 3:
            self.maze1 = self.level_3()
        else:
            gs = Finishscreen3()
            gs.run()

        self.sprite()
        self.prev_sprite_rect = self.sprite_rect.copy()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.cell_x < 14 and self.maze1[self.cell_y][self.cell_x + 1] != 1:
                            self.cell_x += 1
                    elif event.key == pygame.K_LEFT:
                        if self.cell_x > 0 and self.maze1[self.cell_y][self.cell_x - 1] != 1:
                            self.cell_x -= 1
                    elif event.key == pygame.K_UP:
                        if self.cell_y > 0 and self.maze1[self.cell_y - 1][self.cell_x] != 1:
                            self.cell_y -= 1
                    elif event.key == pygame.K_DOWN:
                        if self.cell_y < 6 and self.maze1[self.cell_y + 1][self.cell_x] != 1:
                            self.cell_y += 1

                    if self.maze1[self.cell_y][self.cell_x] == -1:
                        self.handle_black_hole()
                        
                self.sprite_position()
                if self.cell_x == self.target_cell_x and self.cell_y == self.target_cell_y:
                    self.running = False
                    self.stop1()

            self.time_left -= self.clock.get_time() / 1000
            if self.time_left <= 0:
                self.running = False
                self.stop()

            self.screen.blit(self.fon, self.prev_sprite_rect.topleft, area=self.prev_sprite_rect)
            self.screen.blit(self.grid_surface, self.prev_sprite_rect.topleft, area=self.prev_sprite_rect)

            self.screen.blit(self.sprite_image, self.sprite_rect)

            self.screen.blit(self.fon, self.timer_rect.topleft, area=self.timer_rect)
            timer_text = self.font.render(f"Time: {int(self.time_left)}", True, (255, 255, 255))
            self.screen.blit(timer_text, (10, 10))

            self.prev_sprite_rect = self.sprite_rect.copy()

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def sprite(self):
        self.sprite_image = pygame.image.load("img/rb_57458.png").convert_alpha()
        original_width = self.sprite_image.get_width()
        original_height = self.sprite_image.get_height()

        new_width = 100
        new_height = 100

        if original_width > original_height:
            new_height = int((original_height / original_width) * new_width)
        else:
            new_width = int((original_width / original_height) * new_height)

        self.sprite_image = pygame.transform.smoothscale(self.sprite_image, (new_width, new_height))

        self.sprite_rect = self.sprite_image.get_rect()

        self.cell_width = self.WIDTH // 15
        self.cell_height = self.HEIGHT // 7

        self.cell_x = 0
        self.cell_y = 6

        self.center_x = (self.cell_x * self.cell_width) + (self.cell_width // 2)
        self.center_y = (self.cell_y * self.cell_height) + (self.cell_height // 2)

        self.sprite_rect.center = (self.center_x, self.center_y)

    def sprite_position(self):
        self.center_x = (self.cell_x * self.cell_width) + (self.cell_width // 2)
        self.center_y = (self.cell_y * self.cell_height) + (self.cell_height // 2)
        self.sprite_rect.center = (self.center_x, self.center_y)

    def level_1(self):
        self.maze = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, -1, 0, 1, 1, -1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, -1, 1, 0, 1, 0, -1, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        ]

        self.black_hole_image = pygame.image.load("img/dy.png").convert_alpha()
        self.black_hole_image = pygame.transform.scale(self.black_hole_image, (self.cell_size, self.cell_size))
        self.wall_image = pygame.image.load("img/rb_83361.png").convert_alpha()
        self.wall_image = pygame.transform.scale(self.wall_image, (self.cell_size, self.cell_size))

        for row in range(7):
            for col in range(15):
                if self.maze[row][col] == 1:
                    self.screen.blit(
                        self.wall_image,
                        (col * self.cell_size, row * self.cell_size)
                    )
                elif self.maze[row][col] == -1:
                    self.screen.blit(
                        self.black_hole_image,
                        (col * self.cell_size, row * self.cell_size)
                    )
        return self.maze

    def level_2(self):
        self.maze = [
            [0, 0, 0, 0, 0, 0, 1, 1, 0, -1, 0, 0, 0, 1, 0],
            [0, 1, -1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0],
            [0, 1, 1, 1, 0, -1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        ]

        self.black_hole_image = pygame.image.load("img/dy.png").convert_alpha()
        self.black_hole_image = pygame.transform.scale(self.black_hole_image, (self.cell_size, self.cell_size))
        self.wall_image = pygame.image.load("img/rb_83361.png").convert_alpha()
        self.wall_image = pygame.transform.scale(self.wall_image, (self.cell_size, self.cell_size))

        for row in range(7):
            for col in range(15):
                if self.maze[row][col] == 1:
                    self.screen.blit(
                        self.wall_image,
                        (col * self.cell_size, row * self.cell_size)
                    )
                elif self.maze[row][col] == -1:
                    self.screen.blit(
                        self.black_hole_image,
                        (col * self.cell_size, row * self.cell_size)
                    )
        return self.maze
        
    def level_3(self):
        self.maze = [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
            [0, -1, 0, 1, -1, 0, 0, 0, 1, 0, -1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 1, 0, -1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, -1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.black_hole_image = pygame.image.load("img/dy.png").convert_alpha()
        self.black_hole_image = pygame.transform.scale(self.black_hole_image, (self.cell_size, self.cell_size))
        self.wall_image = pygame.image.load("img/rb_83361.png").convert_alpha()
        self.wall_image = pygame.transform.scale(self.wall_image, (self.cell_size, self.cell_size))

        for row in range(7):
            for col in range(15):
                if self.maze[row][col] == 1:
                    self.screen.blit(
                        self.wall_image,
                        (col * self.cell_size, row * self.cell_size)
                    )
                elif self.maze[row][col] == -1:
                    self.screen.blit(
                        self.black_hole_image,
                        (col * self.cell_size, row * self.cell_size)
                    )
        return self.maze

    def find_random_free_cell(self):
        free_cells = []
        for row in range(len(self.maze1)):
            for col in range(len(self.maze1[row])):
                if self.maze1[row][col] == 0:
                    free_cells.append((row, col))
        if free_cells:
            return random.choice(free_cells)
        return None

    def handle_black_hole(self):
        free_cell = self.find_random_free_cell()
        if free_cell:
            self.cell_y, self.cell_x = free_cell
            self.sprite_position()

    def stop(self):
        gs = Finishscreen1()
        gs.run()

    def stop1(self):
        gs = Finishscreen2()
        gs.run()

    def terminate(self):
        pygame.quit()
        sys.exit()

class Finishscreen1:
    def  __init__(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (102, 186, 168)
        self.RED = (229, 0, 95)
        self.BLUE = (0, 0, 150)

        self.FPS = 50
        self.clock = pygame.time.Clock()
        self.start_screen()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Космический доставщик пиццы")
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetWindowPos(hwnd, 0, 400, 100, 0, 0, 0x0001)
        fon = pygame.transform.scale(pygame.image.load('img/kosmos-77.webp'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        font = pygame.font.Font(None, 50)
        text = font.render("Вы опоздали :(", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 200))
        screen.blit(text, text_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            self.draw_button(screen, "Попробовать еще раз", 150, 350, 250, 50, self.BLUE, self.GREEN, lambda: self.start_game())
            self.draw_button(screen, "Перейти в главную", 450, 350, 250, 50, self.BLUE, self.RED, lambda: self.start_game2())

            pygame.display.flip()
            self.clock.tick(self.FPS)
        
    def draw_button(self, screen, text, x, y, width, height, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            pygame.draw.rect(screen, hover_color, (x, y, width, height))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, color, (x, y, width, height))

        font = pygame.font.Font(None, 30)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surface, text_rect)

    def start_game(self):
        gs = GameScreen()
        gs.run()

    def start_game2(self):
        gs = StartScreen()
        gs.run()


class Finishscreen2:
    def  __init__(self):
        self.GREEN = (102, 186, 168)
        self.RED = (229, 0, 95)
        self.BLUE = (0, 0, 150)
        self.WHITE = (255, 255, 255)

        self.FPS = 50
        self.clock = pygame.time.Clock()
        self.start_screen()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Космический доставщик пиццы")
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetWindowPos(hwnd, 0, 400, 100, 0, 0, 0x0001)
        fon = pygame.transform.scale(pygame.image.load('img/kosmos-77.webp'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        con = sqlite3.connect('kosmicheskiy_dostavshchik_pitstsy.db')
        cur = con.cursor()

        cur.execute("UPDATE player SET level = level + 1")
        cur.execute("UPDATE player SET points = points + 10")
        cur.execute("SELECT points FROM player")
        result = cur.fetchone()[0]
        
        con.commit()

        font = pygame.font.Font(None, 50)
        text = font.render('Пицца доставлена вовремя :)', True, (255, 255, 255))
        
        text_rect = text.get_rect(center=(WIDTH // 2, 200))
        screen.blit(text, text_rect)

        text = font.render(f'У вас теперь: {result} очков', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 250))
        screen.blit(text, text_rect)

        image = pygame.image.load('img/pizza.png')
        image = pygame.transform.scale(image, (110, 110))
        image_rect = image.get_rect(center=(WIDTH // 2, 100))
        screen.blit(image, image_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            self.draw_button(screen, "Продолжить", 150, 350, 250, 50, self.BLUE, self.GREEN, lambda: self.start_game())
            self.draw_button(screen, "Перейти в главную", 450, 350, 250, 50, self.BLUE, self.RED, lambda: self.start_game2())

            pygame.display.flip()
            self.clock.tick(self.FPS)
        
    def draw_button(self, screen, text, x, y, width, height, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            pygame.draw.rect(screen, hover_color, (x, y, width, height))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, color, (x, y, width, height))

        font = pygame.font.Font(None, 30)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surface, text_rect)

    def start_game(self):
        gs = GameScreen()
        gs.run()

    def start_game2(self):
        gs = StartScreen()
        gs.run()


class Finishscreen3:
    def  __init__(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (102, 186, 168)
        self.RED = (229, 0, 95)
        self.BLUE = (0, 0, 150)

        self.FPS = 50
        self.clock = pygame.time.Clock()
        self.start_screen()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Космический доставщик пиццы")
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetWindowPos(hwnd, 0, 400, 100, 0, 0, 0x0001)
        fon = pygame.transform.scale(pygame.image.load('img/kosmos-77.webp'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
    
        font = pygame.font.Font(None, 50)
        text = font.render("Игра закончена", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 200))
        screen.blit(text, text_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

            self.draw_button(screen, "Перейти в главную", 270, 300, 250, 50, self.BLUE, self.RED, lambda: self.start_game())

            pygame.display.flip()
            self.clock.tick(self.FPS)
        
    def draw_button(self, screen, text, x, y, width, height, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            pygame.draw.rect(screen, hover_color, (x, y, width, height))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, color, (x, y, width, height))

        font = pygame.font.Font(None, 30)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surface, text_rect)

    def start_game(self):
        gs = StartScreen()
        gs.run()



if __name__ == "__main__":
    app = StartScreen()
    app.run()
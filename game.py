import pygame
from pygame.locals import *
import time
import random

SIZE = 25


class Candy:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/candy.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*5
        self.y = SIZE*5

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 38)*SIZE
        self.y = random.randint(0, 26)*SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [0]*length
        self.y = [50]*length
        self.direction = 'right'

    def increase_len(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] = (self.y[0] - SIZE) % 690
        if self.direction == 'down':
            self.y[0] = (self.y[0] + SIZE) % 690
        if self.direction == 'left':
            self.x[0] = (self.x[0] - SIZE) % 1000
        if self.direction == 'right':
            self.x[0] = (self.x[0] + SIZE) % 1000
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 700))
        self.surface.fill((59, 18, 18))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.candy = Candy(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def display_score(self):
        font = pygame.font.SysFont('Corbel', 25, False, True)
        score = font.render(f"Score: {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(score, (10, 10))

    def play_background_music(self):
        pygame.mixer.music.load("resources/gameMusic.mp3")
        pygame.mixer.music.play(-1)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.candy.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with candy
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.candy.x, self.candy.y):
            self.play_sound("eat")
            self.candy.move()
            self.snake.increase_len()

        # snake colliding with candy
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise

    def show_game_over(self):
        self.render_background()
        pygame.mixer.music.pause()
        self.play_sound("gameOver")
        font = pygame.font.SysFont('Corbel', 30, False, True)
        text = font.render(f"Game Over! Your score is {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(text, (60, 100))
        text2 = font.render("Press ENTER to play again. Press ESCAPE to exit", True, (255, 255, 255))
        self.surface.blit(text2, (60, 150))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.candy = Candy(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.17)


if __name__ == "__main__":
    game = Game()
    game.run()


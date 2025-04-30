import pygame
from pygame.math import Vector2
import random
import sys

pygame.init()

# dimensions of the grid (number of squares)
griddims = 20
# size of each square, in pixels
gridsize = 40

# set up player score
score = 0

# set up the window
window = pygame.display.set_mode((griddims * gridsize, griddims * gridsize))
pygame.display.set_caption("Snake Simulator: Become The Python")

# set up font for score display
font = pygame.font.Font(None, 36)

# font rendering function
def draw_text(text, font, textcolor, x, y):
    img = font.render(text, True, textcolor)
    window.blit(img, (x, y))

# set up controller for alternative input
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        # start moving to the right
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        for sq in self.body:
            snakesq = pygame.Rect(int(sq.x) * gridsize, int(sq.y) * gridsize, gridsize, gridsize)
            pygame.draw.rect(window, (255, 255, 255), snakesq)

    def slither(self, fruitpos):
        global score
        # move the snake in the current direction
        new_head = self.body[0] + self.direction

        # if the snake collides with the edge of the window, the game ends
        if new_head.x >= griddims or new_head.x < 0 or new_head.y >= griddims or new_head.y < 0:
            return False
        
        # if the snake collides with its body, the game ends
        for sq in self.body:
            if new_head == sq:
                return False

        # if the snake collides with a fruit, eat it and grow the snake
        if new_head == fruitpos:
            self.body.append(self.body[-1])
            fruit.grow_fruit()
            score += 1
        else:
            # add new head
            self.body.insert(0, new_head)
            # remove the last segment
            self.body.pop()
        
        # return True if the snake is still alive
        return True

    def change_direction(self, new_dir):
        # prevent the snake from reversing
        if (new_dir.x * -1, new_dir.y * -1) != (self.direction.x, self.direction.y):
            self.direction = new_dir

    def move_snake(self, event_list):
        input_processed = False  # Flag to track if input has been processed

        for e in event_list:
            if input_processed:
                # if there was an input on the current frame, don't process any more (avoids rapid inputs resulting in game over)
                break

            if e.type == pygame.KEYDOWN:
                # get the key input
                if e.key == pygame.K_UP or e.key == pygame.K_w:
                    self.change_direction(Vector2(0, -1))
                    # mark input as processed
                    input_processed = True
                elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                    self.change_direction(Vector2(0, 1))
                    input_processed = True
                elif e.key == pygame.K_LEFT or e.key == pygame.K_a:
                    self.change_direction(Vector2(-1, 0))
                    input_processed = True
                elif e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                    self.change_direction(Vector2(1, 0))
                    input_processed = True
                
            if e.type == pygame.JOYAXISMOTION and not input_processed:
                # get the joystick axis values
                x_axis = pygame.joystick.Joystick(0).get_axis(0)
                y_axis = pygame.joystick.Joystick(0).get_axis(1)

                # check for significant movement on the axes
                if y_axis < -0.5:
                    self.change_direction(Vector2(0, -1))
                    input_processed = True
                elif y_axis > 0.5:
                    self.change_direction(Vector2(0, 1))
                    input_processed = True
                elif x_axis < -0.5:
                    self.change_direction(Vector2(-1, 0))
                    input_processed = True
                elif x_axis > 0.5:
                    self.change_direction(Vector2(1, 0))
                    input_processed = True

class Fruit:
    def __init__(self):
        self.grow_fruit()

    def grow_fruit(self):
        while True:
            # random position, keep the fruit on the displayed area
            self.x = random.randint(0, griddims - 1)
            self.y = random.randint(0, griddims - 1)
            self.pos = Vector2(self.x, self.y)

            # check if the new position is not on the snake's body
            if self.pos not in snake.body:
                # if it is not on the snake's body, exit the loop
                break

    def draw_fruit(self):
        # size and position of the fruit
        fruitsq = pygame.Rect(int(self.pos.x * gridsize), int(self.pos.y * gridsize), gridsize, gridsize)
        # draw the fruit
        pygame.draw.rect(window, (255, 0, 0), fruitsq)

# set up time and game-relevant entities
clock = pygame.time.Clock()
snake = Snake()
fruit = Fruit()

# game loop
game_over = False
while True:
    event_list = pygame.event.get()

    for event in event_list:
        # enable quitting
        if event.type == pygame.QUIT:
            sys.exit()

    if not game_over:
        # move the snake based on input
        snake.move_snake(event_list)

        # move the snake and check for collisions
        if not snake.slither(Vector2(fruit.x, fruit.y)):
            game_over = True

        # background
        window.fill((0, 0, 0))

        # draw the snake and fruit
        snake.draw_snake()
        fruit.draw_fruit()

        # draw the score
        draw_text(str(score), font, (255, 255, 255), 770, 10)

    else:
        # display Game Over message
        draw_text("Game Over", font, (255, 0, 0), griddims * gridsize // 2 - 50, griddims * gridsize // 2)
        draw_text("Press 'R' to Restart", font, (255, 255, 255), griddims * gridsize // 2 - 80, griddims * gridsize // 2 + 40)

        # check for restart input
        for e in event_list:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    # reset the game state
                    score = 0
                    snake = Snake()
                    fruit = Fruit()
                    game_over = False

    pygame.display.update()
    
    # set the speed of the snake
    clock.tick(10)

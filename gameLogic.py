import pygame
import sys
import random
from pygame.math import Vector2


# Create grid-like pattern
cell_size = 25
cell_number = 25


# Initiate screen (width / height)
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))


# Graphics food
apple_png = pygame.image.load('Graphics/apple.png').convert_alpha()
apple_png = pygame.transform.scale(apple_png, (cell_size, cell_size))


# Graphics snake
snake_head = pygame.image.load('Graphics/head_up.png').convert_alpha()
snake_head_up = pygame.transform.scale(snake_head, (cell_size, cell_size))
snake_head_left = pygame.transform.rotate(snake_head_up, 90)
snake_head_down = pygame.transform.rotate(snake_head_up, 180)
snake_head_right = pygame.transform.rotate(snake_head_up, 270)

snake_tail = pygame.image.load('Graphics/tail_up.png').convert_alpha()
snake_tail_up = pygame.transform.scale(snake_tail, (cell_size, cell_size))
snake_tail_left = pygame.transform.rotate(snake_tail_up, 90)
snake_tail_down = pygame.transform.rotate(snake_tail_up, 180)
snake_tail_right = pygame.transform.rotate(snake_tail_up, 270)

snake_body = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
snake_body_vertical = pygame.transform.scale(snake_body, (cell_size, cell_size))
snake_body_horizontal = pygame.transform.rotate(snake_body_vertical, 90)

snake_bend = pygame.image.load('Graphics/body_bl.png').convert_alpha()
snake_bend_bl = pygame.transform.scale(snake_bend, (cell_size, cell_size))
snake_bend_br = pygame.transform.rotate(snake_bend_bl, 90)
snake_bend_tl = pygame.transform.rotate(snake_bend_bl, 180)
snake_bend_tr = pygame.transform.rotate(snake_bend_bl, 270)



# --------------------------------------------------------------------------------------------------------------- #


class Fruit:
    def __init__(self) -> None:
        self.position_fruit()


    def draw_fruit(self):
        fruit_rect = pygame.Rect((self.pos.x  * cell_size, self.pos.y  * cell_size), (cell_size, cell_size))
        # pygame.draw.rect(surface=screen, color=(255,0,0), rect=fruit_rect)
        screen.blit(apple_png, fruit_rect)

    def position_fruit(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(5,8), Vector2(4,8), Vector2(3,8)]
        self.movement = Vector2(1, 0)


    def draw_snake(self):
        self.snake_head_position_determiner()
        self.snake_tail_position_determiner()

        for index, segment in enumerate(self.body):
            x_pos = segment.x * cell_size
            y_pos = segment.y * cell_size
            snake_rect = pygame.Rect((x_pos, y_pos), (cell_size, cell_size))

            if index == 0:
                screen.blit(self.snake_head_position, snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.snake_tail_position, snake_rect)
            else:
                previous_segment = self.body[index + 1] - segment
                next_segment = self.body[index - 1] - segment
                if previous_segment.x == next_segment.x:
                    screen.blit(snake_body_vertical, snake_rect)
                elif previous_segment.y == next_segment.y:
                    screen.blit(snake_body_horizontal, snake_rect)
                else:
                    if previous_segment.x == 1 and next_segment.y == 1 or previous_segment.y == 1 and next_segment.x == 1:
                        screen.blit(snake_bend_br, snake_rect)
                    elif previous_segment.x == -1 and next_segment.y == 1 or previous_segment.y == 1 and next_segment.x == -1:
                        screen.blit(snake_bend_bl, snake_rect)
                    elif previous_segment.x == 1 and next_segment.y == -1 or previous_segment.y == -1 and next_segment.x == 1:
                        screen.blit(snake_bend_tl, snake_rect)
                    elif previous_segment.x == -1 and next_segment.y == -1 or previous_segment.y == -1 and next_segment.x == -1:
                        screen.blit(snake_bend_tr, snake_rect)



    def snake_head_position_determiner(self):
        head_position_calculation = self.body[1] - self.body[0]
        if head_position_calculation == Vector2(1,0):
            self.snake_head_position = snake_head_left
        elif head_position_calculation == Vector2(-1,0):
            self.snake_head_position = snake_head_right
        elif head_position_calculation == Vector2(0,1):
            self.snake_head_position = snake_head_up
        elif head_position_calculation == Vector2(0,-1):
            self.snake_head_position = snake_head_down

    def snake_tail_position_determiner(self):
        tail_position_calculation = self.body[-2] - self.body[-1]
        if tail_position_calculation == Vector2(1,0):
            self.snake_tail_position = snake_tail_left
        elif tail_position_calculation == Vector2(-1,0):
            self.snake_tail_position = snake_tail_right
        elif tail_position_calculation == Vector2(0,1):
            self.snake_tail_position = snake_tail_up
        elif tail_position_calculation == Vector2(0,-1):
            self.snake_tail_position = snake_tail_down

    def move_snake(self):
        body_copy = self.body[:-1]
        head = self.body[0] + self.movement
        body_copy.insert(0, head)
        self.body = body_copy[:]


    def draw_grass(self):
        grass_color = (193, 243, 118)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect((col * cell_size, row * cell_size), (cell_size, cell_size))
                        pygame.draw.rect(surface=screen, color=grass_color, rect=grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect((col * cell_size, row * cell_size), (cell_size, cell_size))
                        pygame.draw.rect(surface=screen, color=grass_color, rect=grass_rect)


class Logic:
    def __init__(self) -> None:
        self.snake = Snake()
        self.fruit = Fruit()

    
    def update(self):
        self.snake.move_snake()
        self.eat_fruit()
        self.out_of_bounds()


    def draw_elements(self):
        self.snake.draw_grass()
        self.draw_score()
        self.snake.draw_snake()
        self.fruit.draw_fruit()


    def eat_fruit(self):
        if self.snake.body[0] == self.fruit.pos:
            self.snake.body.append(self.snake.body[-1])
            self.fruit = Fruit()
            while self.fruit.pos in self.snake.body:
                self.fruit = Fruit()

    
    def out_of_bounds(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()
        
    
    def game_over(self):
            pygame.quit()
            sys.exit()


    def draw_score(self):
        # Font
        game_font = pygame.font.Font('Font\PoetsenOne-Regular.ttf', 25)
        
        score_text = f"{len(self.snake.body) - 3}"
        score_surface = game_font.render(score_text, True, (58, 59, 60))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)
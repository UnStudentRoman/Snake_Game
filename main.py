import pygame
import sys
from pygame.math import Vector2
from gameLogic import Logic, screen


# --------------------------------------------------------------------------------------------------------------- #

# Starts pygame
pygame.init()

# Game initialization
game = Logic()

# clock object will block the framerate.
clock = pygame.time.Clock()
fps = 60

# Timer
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(event=SCREEN_UPDATE, millis=int(75))


# --------------------------------------------------------------------------------------------------------------- #

while True:
    # For loop checks if event recorded is clicking the X button.
    for event in pygame.event.get():
        # print(f'Event looks like this {event}')
        # print(f'Event.type looks like this {event.type}')
        if event.type == pygame.QUIT:

            # Oposite of pygame.init()
            pygame.quit()
            
            # Making sure everything stops after pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and game.snake.movement != Vector2(0, 1):
                game.snake.movement = Vector2(0, -1)
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s)and game.snake.movement != Vector2(0, -1):
                game.snake.movement = Vector2(0, 1)
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game.snake.movement != Vector2(1, 0):
                game.snake.movement = Vector2(-1, 0)
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game.snake.movement != Vector2(-1, 0):
                game.snake.movement = Vector2(1, 0)
                

    # Draw elemets of game.
    screen.fill(color=(161, 223, 80))
    game.draw_elements()


    # Pygame display.update will display all elements drawn.
    pygame.display.update()
    clock.tick(fps)
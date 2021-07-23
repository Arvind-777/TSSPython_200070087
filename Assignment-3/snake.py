import pygame
import sys
import time
import random

# initial game variables

# Window size
frame_size_x = 720
frame_size_y = 480

# Parameters for Snake
square_side = 10
snake_color = (0, 255, 0)
snake_pos = [100, 50]
snake_body = [[100, 50], [100 - square_side, 50], [100 - (2 * square_side), 50]]
direction = 'RIGHT'

# Parameters for food
food_pos = [0, 0]
food_spawned = False
food_color = (255, 255, 255)
food_rect = pygame.Rect(0, 0, square_side, square_side)

score = 0

# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
bg_color = (0, 0, 0)

# FPS (frames per second) controller to set the speed of the game
fps_controller = pygame.time.Clock()


def check_for_events():
    """
    This should contain the main for loop (listening for events). You should close the program when
    someone closes the window, update the direction attribute after input from users. You will have to make sure
    snake cannot reverse the direction i.e. if it turned left it cannot move right next.
    """
    global direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"


def update_snake():
    """
     This should contain the code for snake to move, grow, detect walls etc.
     """
    global food_spawned, score

    snake_last_pos = snake_body[len(snake_body)-1]
    dx, dy = 0, 0

    # Code for making the snake move in the expected direction
    if direction == "RIGHT":
        dx = square_side
        dy = 0
    elif direction == "DOWN":
        dx = 0
        dy = square_side
    elif direction == "LEFT":
        dx = (-1)*square_side
        dy = 0
    elif direction == "UP":
        dx = 0
        dy = (-1)*square_side

    for i in range(len(snake_body)-1, 0, -1):
        snake_body[i] = snake_body[i-1]

    snake_body[0] = [snake_body[0][0] + dx, snake_body[0][1] + dy]

    # Make the snake's body respond after the head moves. The responses will be different if it eats the food.
    # Note you cannot directly use the functions for detecting collisions
    # since we have not made snake and food as a specific sprite or surface.
    if snake_body[0] == food_pos:
        snake_body.append(snake_last_pos)
        food_spawned = False
        score += 1

    # End the game if the snake collides with the wall or with itself.
    for i in range(1, len(snake_body)-1):
        if snake_body[0] == snake_body[i]:
            game_over()

        elif snake_body[0][0] < 0 or snake_body[0][0] > frame_size_x or snake_body[0][1] < 0 \
                or snake_body[0][1] > frame_size_y:
            game_over()


def create_food():
    """
    This function should set coordinates of food if not there on the screen. You can use randrange() to generate
    the location of the food.
    """
    global food_spawned
    if not food_spawned:
        food_pos[0] = random.randrange(0, frame_size_x, square_side)
        food_pos[1] = random.randrange(0, frame_size_y, square_side)
        food_spawned = True
    return food_pos


def show_score(pos, color, font, size):
    """
    It takes in the above arguments and shows the score at the given pos according to the color, font and size.
    """
    score_img = pygame.font.SysFont(font, size).render(f"Score : {score}", True, color)
    score_rect = score_img.get_rect()
    score_rect.centerx = pos[0]
    score_rect.centery = pos[1]
    game_window.blit(score_img, score_rect)


def update_screen():
    """
    Draw the snake, food, background, score on the screen
    """
    global food_pos, food_rect
    game_window.fill(bg_color)

    food_pos = create_food()
    food_rect.centerx = food_pos[0]
    food_rect.centery = food_pos[1]
    pygame.draw.rect(game_window, food_color, food_rect)

    for pos in snake_body:
        rect = pygame.Rect(0, 0, square_side, square_side)
        rect.centerx = pos[0]
        rect.centery = pos[1]
        pygame.draw.rect(game_window, snake_color, rect)

    show_score([80, 20], (255, 255, 255), None, 20)

    pygame.display.flip()


def game_over():
    """
    Write the function to call in the end.
    It should write game over on the screen, show your score, wait for 3 seconds and then exit
    """
    game_window.fill(bg_color)

    gameover_img = pygame.font.SysFont(None, 48).render("GAME OVER", True, (240, 0, 0))
    gameover_rect = gameover_img.get_rect()
    gameover_rect.centerx = int(frame_size_x / 2)
    gameover_rect.centery = int(frame_size_y / 2)
    game_window.blit(gameover_img, gameover_rect)

    show_score([gameover_rect.centerx, gameover_rect.centery + 100], (240, 0, 0), None, 24)

    pygame.display.flip()
    time.sleep(3)
    sys.exit(0)


# Main loop
while True:
    # Make appropriate calls to the above functions so that the game could finally run
    check_for_events()
    update_snake()
    update_screen()
    # To set the speed of the screen
    fps_controller.tick(25)

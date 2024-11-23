import pygame
import random

pygame.init()

# game settings
tile_size = 32
screen_width, screen_height = 30, 20
background_color = "black"
grid_color = "#323232"
snake_color = "blue"
food_color = "red"
snake_speed = 5
game_font = pygame.font.SysFont("consolas", int(tile_size * screen_width / 30))

# width = tile size * screen width, height = tile size * screen height, 960x640 by default
screen = pygame.display.set_mode((tile_size * screen_width, tile_size * screen_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
running = True
game_over = False

# start with snake moving right
direction = "R"

score = 0

# create snake's head rect (start on coordinates (6, 3), for tile size 32 - Rect(160, 64, 32, 32)
head_rect = pygame.Rect(tile_size * 5, tile_size * 2, tile_size, tile_size)

# create tail list (3 elements - at the back of snake's head)
# for tile size 32 - Rect(128, 64, 32, 32), Rect(96, 64, 32, 32), Rect(32, 64, 32, 32)
tail = [pygame.Rect(i, tile_size * 2, tile_size, tile_size)
        for i in range(tile_size * 4,  tile_size * 2 - 1, -1 * tile_size)]

# create food list
food_list = []

while running:
    # more points - higher speed
    clock.tick(snake_speed + int(score/10))

    if not game_over:
        # to prevent from moving more than once in a frame
        can_move = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # change snake direction
            elif event.type == pygame.KEYDOWN and can_move:
                if event.key == pygame.K_d and direction != "L":
                    direction = "R"
                    can_move = False
                elif event.key == pygame.K_a and direction != "R":
                    direction = "L"
                    can_move = False
                elif event.key == pygame.K_w and direction != "D":
                    direction = "U"
                    can_move = False
                elif event.key == pygame.K_s and direction != "U":
                    direction = "D"
                    can_move = False

        # tail movement
        last_tail_square = tail.pop(-1)  # delete last square and store it (square will be added at the end of the snake after eating food)
        tail.insert(0, head_rect.copy())  # insert new square (previous head position) at front

        # snake head movement (increase by tile size: 32)
        if direction == "R":
            head_rect.x += tile_size
        elif direction == "L":
            head_rect.x -= tile_size
        elif direction == "U":
            head_rect.y -= tile_size
        elif direction == "D":
            head_rect.y += tile_size

        # draw the black background and the grid
        screen.fill(background_color)
        for i in range(-1, tile_size * screen_width, tile_size):
            pygame.draw.line(screen, grid_color, (i, 0), (i, tile_size * screen_height), 2)
        for i in range(-1, tile_size * screen_height, tile_size):
            pygame.draw.line(screen, grid_color, (0, i), (tile_size * screen_width, i), 2)

        # add food if the food list is empty
        # rect for tile size 32, screen width 30 and screen height 20:
        # rect x position in range (0, 929, 32): 929 - (tile size * (screen width - 1)) + 1
        # rect y position: in range (0, 609, 32): 609 - (tile size * (screen height - 1)) + 1
        if len(food_list) < 1:
            food_list.append(pygame.Rect(random.randrange(0, tile_size * (screen_width - 1) + 1, tile_size),
                                         random.randrange(0, tile_size * (screen_height - 1) + 1, tile_size),
                                         tile_size, tile_size))

        # if the spawned food is located in any of the tail's rects,
        # delete it and generate new food, break if there is no any free squares more (game won)
        while food_list[0] in tail:
            if len(tail) == (screen_width * screen_height) - 1:
                game_over = True
            food_list.remove(food_list[0])
            food_list.append(pygame.Rect(random.randrange(0, tile_size * (screen_width - 1) + 1, tile_size),
                                         random.randrange(0, tile_size * (screen_height - 1) + 1, tile_size),
                                         tile_size, tile_size))

        # draw food
        for food in food_list:
            pygame.draw.rect(screen, food_color, food)

            # if food collides with head, remove the food from the screen and extend the snake
            # (use the previously removed last square from the tail list), add score
            if food.colliderect(head_rect):
                food_list.remove(food)
                tail.append(last_tail_square)
                score += 1

        # game over if snake goes off the screen
        if head_rect.x > tile_size * screen_width - tile_size or head_rect.x < 0:
            game_over = True
        if head_rect.y > tile_size * screen_height - tile_size or head_rect.y < 0:
            game_over = True

        # game over if snake's head goes into tail
        if head_rect in tail:
            game_over = True

        # draw snake head
        pygame.draw.rect(screen, snake_color, head_rect)

        # draw tail squares
        for square in tail:
            pygame.draw.rect(screen, snake_color, square)

    # if game is over
    else:
        # draw the background
        screen.fill(background_color)

        # render the text and blit it
        text = game_font.render(f"Your score: {score}. Press enter to play again.", True, "white")
        screen.blit(text, (screen_width * tile_size / 2 - text.get_width() / 2, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # enter to play again
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # set starting values
                    game_over = False
                    direction = "R"
                    score = 0
                    head_rect = pygame.Rect(tile_size * 5, tile_size * 2, tile_size, tile_size)
                    tail = [pygame.Rect(i, tile_size * 2, tile_size, tile_size)
                            for i in range(tile_size * 4, tile_size * 2 - 1, -1 * tile_size)]
                    food_list = []

    # update the screen
    pygame.display.update()

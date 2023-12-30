# Manisha Chaudhary
# ----------------------------------------------------------------------------------------------------------------------
# SNAKE GAME
# ----------------------------------------------------------------------------------------------------------------------

# This is a recreation of the classic snake game where the user controls a snake using up, down, left, and
# right arrows in an attempt to collect apples and grow longer.  If the snake collides with the walls or itself then the game is over and the score is recorded. The
# goal is to collect the most apples and score the highest score.

# 3 BASIC FEATURES:
# User Input: keyboard- up arrow, down arrow, left arrow, right arrow + using mousepad for starting game
# Game Over: If the snake collides with the walls or itself then the game is over and the score is recorded.
# Graphics/Images: apple image from : http://clipart-library.com/clipart/2076315.htm

# 4 BASIC FEATURES:
# Restart from Game Over - When the player gets game over, they can hit a button to restart the game from the beginning. Previous highest score will still be recorded though.
# Collectibles - As the user collects apples, the snake increases in length and the point count increases.
# Sprite sheet - confetti animation every time high score is beat - (sheet from : https://opengameart.org/content/confetti-effect-spritesheet)
# Something More - stores the highest score despite how many times the player plays the game and it always updates if a higher score is scored

# ----------------------------------------------------------------------------------------------------------------------

import uvage
import random

# screen
width = 800
height = 600
camera = uvage.Camera(width, height)

snake_position = [125, 50]  # default start position

# first 4 blocks of snake body
# list of lists that act as coordinate points
snake_body = [[50, 50],
              [75, 50],
              [100, 50],
              [125, 50]
              ]
head_list = []  # empty list which will be filled with green square objects
# fruit position - generated using random function
fruit_position = [
    random.randrange(25, width - 25, 25),
    random.randrange(25, height - 25, 25)
]
fruit = True  # existance of fruit - if false then generates new fruit at rondom location

# default snake direction is right
direction = "right"
change = direction

# score trackers
high_score = 0
score = 0

# sprite animation of confetti
confetti = uvage.load_sprite_sheet("Confetti.png", 8, 8)
base = uvage.from_image(width / 2, height - 10, confetti[-1])
current_frame = 0

# game over boolean and beating high score boolean
over = False
beat = False


# displaying Score function
def display_score():
    """
    displays the current score at bottom left corner of screen
    :return: no return
    """
    camera.draw(str(int(score)), 30, "red", 60, height - 60)


def restart():
    """
    resets all values to their original value to restart game
    :return: no return
    """
    # identifying all global variables
    global direction, change, snake_position, fruit_position, fruit, over, score, high_score, snake_body, current_frame, beat

    camera.clear("white")
    snake_position = [125, 50]  # default start position

    # first 4 blocks of snake body
    snake_body.clear()
    snake_body = [[50, 50],
                  [75, 50],
                  [100, 50],
                  [125, 50]
                  ]
    # fruit position
    fruit_position = [
        random.randrange(25, width - 25, 25),
        random.randrange(25, height - 25, 25)
    ]
    fruit = True
    direction = "right"
    change = direction
    score = 0
    over = False
    beat = False
    current_frame = 0


def celebrate():
    """
    runs confetti animation using sprite sheet when high score is beat
    :return: no return
    """
    global beat, current_frame, confetti, base
    if beat:
        current_frame += 10
        if current_frame < 64:
            base.image = confetti[int(current_frame)]
    camera.draw(base)


def movement():
    """
    this function handles all snake movement(user input with arrow keys), updating the snake body, ensuring the snake can't move in opposite directions at the same time, and drawing the snake and apple
    :return: no return
    """
    global direction, change, snake_position, fruit_position, fruit, over, score, snake_body, head_list
    if not over:
        camera.clear("white")
        fruit = True
        head_list = []
        if snake_position[0] % 25 == 0 and snake_position[
            1] % 25 == 0:  # using mod25 to make sure that snake position can only change at certain grid locations (kind of like viewing 25x25 pixels as 1 pixel)
            # when user is pressing arrow keys the variable 'change' is updated
            if uvage.is_pressing("right arrow"):
                change = "right"
            if uvage.is_pressing("left arrow"):
                change = "left"
            if uvage.is_pressing("up arrow"):
                change = "up"
            if uvage.is_pressing("down arrow"):
                change = "down"

        # draws 25x25 box at every point in the snake body list
        for position in snake_body:
            head = (uvage.from_color(position[0], position[1], "green", 25, 25))
            camera.draw(head)
            head_list.append(head)
            # adds every object(green square) into an empty list (called head_list)

        # draws apple at fruit position which was previously determined using the random function
        apple = (uvage.from_image(fruit_position[0], fruit_position[1], "apple - Copy.png"))  # image of apple
        apple.scale_by(0.1)
        camera.draw(apple)

        # If two keys pressed simultaneously
        # don't want snake to move into two directions at the same time - ex: if the snake is moving up, pressing the down arrow will do nothing
        if change == 'up' and direction != 'down':
            direction = 'up'
        if change == 'down' and direction != 'up':
            direction = 'down'
        if change == 'left' and direction != 'right':
            direction = 'left'
        if change == 'right' and direction != 'left':
            direction = 'right'

        # move snake by changing snake position(x or y depending on left/right or up/down)
        # adds the current head position to the snake_body list
        if direction == 'down':
            snake_position[1] += 25  # changing y position of the head piece (snake_position)
            snake_body.append(list(snake_position))  # adding this new coordinate to snake_body
        if direction == 'up':
            snake_position[1] -= 25
            snake_body.append(list(snake_position))
        if direction == 'right':
            snake_position[0] += 25
            snake_body.append(list(snake_position))
        if direction == 'left':
            snake_position[0] -= 25
            snake_body.append(list(snake_position))

        snake_body.pop(
            0)  # removes the first list(coordinate point) from the snake_body list - basically removing the tail piece

        # HOW THIS WORKS:
        # essentially, every time the snake moves by 25 pixels this is the new current head position (called snake_position)
        # when this new position is added to the end of snake_body list, the first list (coordinate of tail piece) in the snake_body list is removed
        # meaning whenever a list is added to the end of the list, the list at index 0 is removed
        # this makes it look like the snake is moving when really the locations of the green square objects are being changed
        # if this is still confusing just use 'print(snake_body)' to see how the list is changing

        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            # increases length of snake by adding the snake position to snake_body list without removing the tail piece
            score += 1
            snake_body.append(list(snake_position))
            fruit = False


def tick():
    """
    main tick function which runs 9 times per second and calls other functions
    :return: no return
    """
    global snake_position, fruit_position, fruit, over, score, high_score, beat, head_list

    if not over:  # runs when game is not over

        movement()  # calling movement function which controls the body of the snake

        # if apple is not present then this generates a new apple at a new random location
        if not fruit:
            fruit_position = [
                random.randrange(25, width - 25, 25),
                random.randrange(25, height - 25, 25)
            ]

        # Game Over if snake touches edges of screen
        if snake_position[0] < 0 or snake_position[0] > width:
            over = True

        if snake_position[1] < 0 or snake_position[1] > height:
            over = True

        # game over if snake collides with snake body
        # if the snake's current head position is at any point where there is green box object(body of snake) then game over
        for piece in head_list[:]:
            if piece.contains(snake_position[0], snake_position[1]):
                over = True

        # if the current score is higher tha previous high score then boolean beat becomes true and high score is updated
        if score > high_score:
            high_score = score
            beat = True

    # when game is over the screen turns black, current score and high score is displayed, the user is prompted to restart
    # celebrate function is called if the high score was beat
    if over:
        camera.clear("black")
        camera.draw("Your score is: " + str(score), 50, "red", width / 2, height / 2)  # current score
        camera.draw("High score: " + str(high_score), 30, "red", width / 2, height / 2 + 100)  # overall high score
        camera.draw(uvage.from_text(400, 200, "Press R to restart!", 50, "Green"))

        if beat:  # high score topped
            celebrate()
    if uvage.is_pressing("r") and over:  # if user presses r then restart function is called and the game restarts
        restart()

    display_score()
    camera.display()


uvage.timer_loop(9, tick)

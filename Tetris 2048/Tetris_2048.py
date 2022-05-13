import stddraw  # the stddraw module is used as a basic graphics library
import random  # used for creating tetrominoes with random types/shapes
from game_grid import GameGrid  # class for modeling the game grid
from tetromino import Tetromino  # class for modeling the tetrominoes
from picture import Picture  # used representing images to display
import os  # used for file and directory operations
from color import Color  # used for coloring the game menu
import wave
from playsound import playsound
from multiprocessing import Process
# MAIN FUNCTION OF THE PROGRAM
# -------------------------------------------------------------------------------
# Main function where this program starts execution

def start():
    # set the dimensions of the game grid

    music = Process(target=musicJob, args=())
    music.start()

    grid_h, grid_w = 22, 12
    # set the size of the drawing canvas
    canvas_h, canvas_w = 33 * grid_h, 50 * grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system
    stddraw.setXscale(-0.5, grid_w + 6)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    stddraw.text(grid_w-1, grid_h-1, "ehe")


    # create the game grid
    grid = GameGrid(grid_h, grid_w)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino(grid_h, grid_w)
    grid.current_tetromino = current_tetromino

    # display a simple menu before opening the game
    display_game_menu(grid_h, grid_w)

    isPaused = False
    # main game loop (keyboard interaction for moving the tetromino)

    while True:

        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()

            if mouse_x >= 13 and mouse_x <= 13 + 3:
                if mouse_y >= 2 and mouse_y <= 2 + 2:
                    isPaused = not isPaused

            if mouse_x >= 13 and mouse_x <= 13 + 3:
                if mouse_y >= 5 and mouse_y <= 5 + 2:
                    print("Ghost Button")

            if mouse_x >= 17 and mouse_x <= 17 + 1:
                if mouse_y >= 20.4 and mouse_y <= 20.4 + 1:
                    music.kill()
                    exit()

        if not isPaused:
            if stddraw.hasNextKeyTyped():
                key_typed = stddraw.nextKeyTyped()
                # if the left arrow key has been pressed
                if key_typed == "left":
                    # move the tetromino left by one
                    current_tetromino.move(key_typed, grid)
                # if the right arrow key has been pressed
                elif key_typed == "right":
                    # move the tetromino right by one
                    current_tetromino.move(key_typed, grid)
                # if the down arrow key has been pressed
                elif key_typed == "down":
                    # move the tetromino down by one
                    # (causes the tetromino to fall down faster)
                    current_tetromino.move(key_typed, grid)
                # clear the queue that stores all the keys pressed/typed
                elif key_typed == "space":
                    current_tetromino.rotate(key_typed, grid)
                elif key_typed == 'p':
                    isPaused = not isPaused

                stddraw.clearKeysTyped()

        # check user interactions via the keyboard


        if isPaused:
            grid.display()
            continue

        # move (drop) the tetromino down by 1 at each iteration
        success = current_tetromino.move("down", grid)

        # place the tetromino on the game grid when it cannot go down anymore
        if not success:
            # get the tile matrix of the tetromino
            tiles_to_place = current_tetromino.tile_matrix
            # update the game grid by adding the tiles of the tetromino
            game_over = grid.update_grid(tiles_to_place)

            didMoved = True
            didMoved2 = True
            didMoved3 = True

            while didMoved or didMoved2 or didMoved3:
                didMoved2 = grid.CheckNumbers()
                didMoved = grid.check_fall2()
                didMoved3 = grid.check_rows()

            grid.SetColors()
            # end the main game loop if the game is over
            if game_over:
                break
            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below
            current_tetromino = create_tetromino(grid_h, grid_w)
            grid.current_tetromino = current_tetromino

        # display the game grid and as well the current tetromino
        grid.display()

    print("Game over")



def musicJob():
    playsound('ehe.mp3')

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
    # type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'S', 'J', 'L', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    # tetromino = Tetromino(random_type, grid_height, grid_width)
    tetromino = Tetromino()
    tetromino.startMethod(random_type, grid_height, grid_width)
    return tetromino


# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
    # colors used for the menu

    background_color = Color(198, 217, 191)
    button_color = Color(40, 114, 113)
    text_color = Color(233, 195, 105)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/tetris_2048_2.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = grid_width - 5, 2
    # coordinates of the bottom left corner of the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Futura Bold")
    stddraw.setFontSize(35)
    stddraw.setPenColor(text_color)
    text_to_display = "START"
    stddraw.text(img_center_x, 5, text_to_display)
    # menu interaction loop
    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked
        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()

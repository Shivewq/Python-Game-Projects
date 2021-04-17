Shiven Sharma
Program: 20 x 10 Tetris Game
Made on VSCode

Sources used:
https://pythonprogramming.net/adding-sounds-music-pygame/ | Sounds found on: https://www.findsounds.com/
Tetris grid: 

Progress Log

To do: 
data structure for pieces (class)
setting up global variables
create score
add instructions
functions needed:
 - create_grid
 - draw_grid
 - draw_window
 - rotating shape in game
 - setting up the main game

4/2

initialized global variables for screen dimensions, grid dimensions & tetris piece sizes

Setup Lists & sublists for each shape & it's rotations, colors 
created a class to initialize & represent actual block pieces, including their size, X & Y positions, assign colors to each shape
*helps with keeping code shorter & organized as well, as these shapes will be called several times

4/3
Started working on functions:
create_grid - represented by using a list of colors. creating a list for every row, 20 sublists for 20 rows
locked_pos as a parameter for current block pieces within this grid
draw_grid - Draw the actual grid
get_shape - simple function using random to choose a shape from shapes list (random.choice)

4/5 
formatting shape lists into readable shapes, + using modulus to get sublists for each shape rotation
Using for loops to find 0s in list for shape format




 
Shiven Sharma
Program: 20 x 10 Tetris Game
Made on VSCode

Sources used:
https://pythonprogramming.net/adding-sounds-music-pygame/ | Sounds found on: https://www.findsounds.com/
Tetris grid: https://www.techwithtim.net/ 

Progress Log (April)

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
Convert lists: 
formatting shape lists into readable shapes, + using modulus to get sublists for each shape rotation
Using for loops to find 0s in list for shape format

COLLISION: 
create a function to find all valid space to move pieces within the grid using color. 
checked by using range similar to grid, & checking if segments are black (0, 0, 0)

4/6
Clearing rows
also uses for loops that reads grid's rows from bottom to top
using colors, if black is not in a row, the increment variable is increased by 1 & row is cleared with try & except
using increment variable to shift down any block pieces above cleared row using locked pos

Created a function to display the upcoming shape after current shape

4/7
Created a simple function for the game grid borders (window)

mainGame
Setting up actual game:
called all needed functions & variables
added a fall speed variable for block pieces
Setup pygame event & key press detection for movement
if statement to trigger piece change + call next piece functions

4/8 
Added some functionality:
added score to drawWindow using string, score updates when clearRows is called in mainGame
added to fall speed of blocks by increasing speed as game goes on in mainGame

4/9
created main menu screen
-Game Title
-Buttons to play the game and view instructions

4/13
added an instructions screen
*add back button 

4/15
Checked code - renamed some variables to simple terms
& adjusted comments

4/16
adjusted functionality 
- speed of blocks (0.20 to 0.30)
changed speed increase as game progresses

"""
Shiven Sharma 
ICS3U1 Ms. Franolla - 4/20/2021
Program: 20 x 10 Tetris Game
"""
infoFile = open('README.txt', 'r')
print(infoFile.read())

#Import Pygame & Mixer
import pygame
import random
#Initialize Pygame & mixer
pygame.init()

#Pygame Screen Caption Name
pygame.display.set_caption('Tetris') 

#Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

#Text Font
titleFont = pygame.font.SysFont("dejavusansmono",38,bold = True)
font = pygame.font.SysFont("dejavusansmono",22,italic = True)
smallFont = pygame.font.SysFont("dejavusansmono",16,italic = True)

#Sound 
pygame.mixer.init()
move_SFX = pygame.mixer.Sound('move.wav')#When moving block pieces
clear_SFX = pygame.mixer.Sound('clear.wav') #When row is cleared
#Adjust volume
move_SFX.set_volume(0.05)
clear_SFX.set_volume(0.05)

#Initialize Global Variables
screen_width = 800
screen_height = 700
play_width = 360  # 300 // 10 = 30 width per block
play_height = 600  # 600 // 20 = 20 height per block
block_size = 30
SIZE = screen_width, screen_height
screen = pygame.display.set_mode(SIZE)

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height

#Center screen
centreX = screen_width / 2
centreY = screen_height / 2
 
pygame.font.init()

#Button Rects
block_width = screen_width // 3
block_height = screen_height // 7

game_Rect = pygame.Rect(block_width, 3*block_height, block_width, block_height)
help_Rect = pygame.Rect(block_width, 5*block_height, block_width, block_height)
back_Rect = pygame.Rect(block_width, 5*block_height, block_width, block_height)

"""
10 x 20 square grid
shapes in lists: S, Z, I, O, J, L, T
"""
# Shape Format + contains sublists for rotations
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T] #Shape list of each Shape format
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)] #Colors for Block Pieces
# index 0 - 6 represent block piece & color respectively 
 
class Piece(object): #Block Pieces positions & color vars
    def __init__(self, x, y, shape):
      self.x = x # x Pos    
      self.y = y # y Pos
      self.shape = shape
      self.color = shape_colors[shapes.index(shape)] #Takes index of shape colors & assigns to respective shape
      self.rotation = 0 # from 0 - 3
 
def createGrid(locked_pos={}): #represent grid using list of colors
    grid = [[(0, 0, 0)for x in range (12)] for x in range(20)] #1 sublist for every row (20 rows) in grid, each containing colors for 10 squares in each row

    for i in range(len(grid)): #length of grid
        for j in range(len(grid[i])): #length of sublist
            if (j, i) in locked_pos: 
               c = locked_pos[(j, i)]
               grid[i][j] = c #find the corresponding position to locked position 

    return grid

#Function draws grid objects (square segments) to see grid & shape structure
def drawGrid(surface, grid): 
    sx = top_left_x
    sy = top_left_y
   
    for i in range(len(grid)): #Length grid (# of rows)
       pygame.draw.line(surface, GRAY, (sx, sy + i*block_size), (sx+play_width, sy + i*block_size)) #20 verticle lines
       for j in range(len(grid[i])): #Length of grid i (# of columns)
          pygame.draw.line(surface, GRAY, (sx + j*block_size, sy), (sx + j*block_size, sy + play_height)) #10 horizontal lines

#Function takes shape as parameter & convert to readable positions
def convertShapeFormat(shape):
  positions = []
  format = shape.shape[shape.rotation % len(shape.shape)] #modulus to access sublists (specific shape) in shape lists
  #Checks Lists' for zeros (0) for actual shape
  for i, line in enumerate(format): 
      row = list(line) #get line in each row
      for j, column in enumerate(row): 
          if column == '0': #add that position to list when 0 found
              positions.append((shape.x + j, shape.y + i)) #current value of shape is added to i / j value when moving 
  
  for i, pos in enumerate(positions): #adjust shape offset for accurate positions (bc removing . in list offsets shapes)
    positions[i] = (pos[0] - 2, pos[1] - 4)
  
  return positions
 
#Function to create all possible movable space
def validSpace(shape, grid): 
    accepted_pos = [[(j, i) for j in range(12) if grid[i][j] == (0,0,0)] for i in range(20)] #all possible positions in 10x20 grid 
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convertShapeFormat(shape) #call shape format to read all possible positions

    for pos in formatted: #loop compares shapes pos & allowed positions which the shape is in
        if pos not in accepted_pos:
            if pos [1] > -1: #allow shapes to be out of screen to spawn there
                return False

    return True #if passes through nested loop

#Function checks if blocks reach/hit the top of screen (game over) 
def checkLost(positions): 
    for pos in positions:
        x, y = pos
        if y < 1:
            return True #Execute function, Lost game

    return False #game stays running
 
#Function passes random shape from shapes list to top of game screen (y Pos = 0)
def getShape(): 
    global shapes, shape_colors
 
    return Piece(5, 0, random.choice(shapes))
 
def textMiddle(text, size, color, surface):
    font = pygame.font.SysFont('dejavusansmono', size, bold=True)
    label = font.render(text, 1, color)
 
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

#Function checks when row cleard, shift every other row above down 
def clearRows(grid, locked): 
    inc = 0
    for i in range(len(grid)-1,-1,-1): #read grid bottom to top
        row = grid[i] #get all rows
        if (0, 0, 0) not in row: #if the color black (empty) is not present in a row
            inc += 1 #increment
            #add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)] #remove locked pos (del row)
                    clear_SFX.play() #play sfx
                except:
                    continue 
    #Shift every row
    if inc > 0: #when row cleared
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]: 
            x, y = key #positions of each key of locked pos
            if y < ind: #to only shift anything ABOVE cleared row
                newKey = (x, y + inc) #new position
                locked[newKey] = locked.pop(key)

    return inc
 
def nextShape(shape, surface):
    title = font.render('Next Shape', 1, WHITE)
    #Positioning
    sx = top_left_x + play_width + 25 
    sy = top_left_y + play_height/2 - 200
    #display next shape using modulus (to display default rotation)
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
 
    surface.blit(title, (sx, sy - 30))
 
def drawWindow(surface, score): #Game border with segments
    surface.fill((BLACK)) #Black Surface
    title = font.render("TETRIS", 1, WHITE) #Title 

    surface.blit(title, (top_left_x + play_width / 2 - (title.get_width() / 2), 30)) #Merge & position top of screen

    title = font.render('Score: ' +str(score), 1, WHITE) #Display score
 
    sx = top_left_x + play_width - 550
    sy = top_left_y + play_height/2 - 380

    surface.blit(title, (sx + 10, sy + 150))

    for i in range(len(grid)): #Draw grid objects
      for j in range(len(grid[i])): #loop through every color in grid (column)
        pygame.draw.rect(surface, grid[i][j], (top_left_x + j* block_size, top_left_y + i * block_size, block_size, block_size), 0) #X & Y Position colors of blocks are being drawn
     
    #Draw grid & border
    drawGrid(surface, grid) #Execute draw_grid Function
    pygame.draw.rect(surface, WHITE, (top_left_x, top_left_y, play_width, play_height), 5)
    pygame.display.update()

#Game screen function
def mainGame(): 
    global grid
 
    locked_positions = {}  # (x,y):(255,0,0)
    grid = createGrid(locked_positions)
 
    runGame = True
    change_piece = False
    current_piece = getShape()
    next_piece = getShape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.30
    level_time = 0
    score = 0
 
    while runGame: 
        grid = createGrid(locked_positions)
        fall_time += clock.get_rawtime() #No FPS as it would mess up block piece speed 
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.008
                 
 
        # Piece falling movment 
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (validSpace(current_piece, grid)) and current_piece.y > 0: #when collides with another piece or ground
                current_piece.y -= 1
                change_piece = True
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                quit()
            #Key detection
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: #move piece left
                    current_piece.x -= 1
                    move_SFX.play()
                    if not validSpace(current_piece, grid):
                        current_piece.x += 1
 
                elif event.key == pygame.K_RIGHT: #move piece right
                    current_piece.x += 1
                    move_SFX.play()
                    if not validSpace(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_UP: #rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    move_SFX.play()
                    if not validSpace(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
 
                elif event.key == pygame.K_DOWN:#skip row (faster fall)
                    current_piece.y += 1
                    move_SFX.play()
                    if not validSpace(current_piece, grid):
                        current_piece.y -= 1
 
        shape_pos = convertShapeFormat(current_piece)
 
        # add piece to the grid for colors (visual)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
 
        # If piece touches the ground or another piece 
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece #Passed next_piece is also passed to current_piece
            next_piece = getShape() #Pass getShape to next_piece
            change_piece = False #back to False until current_piece is placed
            score += clearRows(grid, locked_positions) * 10 # call clearRows to check for multiple clear rows + score
         
 
        drawWindow(win, score)
        nextShape(next_piece, win)
        pygame.display.update()
 
        # Check if user lost
        if checkLost(locked_positions):
            runGame = False
 
    textMiddle("You Lost!", 40, WHITE, win)
    pygame.display.update()
    pygame.time.delay(2000)

#Instructions screen function
def instructions():
    runHelp = True
    #button state
    button = 0
    #mouse Position
    mouseX = 0
    mouseY = 0
    
    while runHelp:
        win.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runHelp = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                button = event.button

            if event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
        
        rect = back_Rect
        pygame.draw.rect(screen, WHITE, rect)
        text = font.render("Back", True, BLACK)
        text_width, text_height = font.size("Back")
        centre_width = (block_width - text_width)//2 #Text centering
        centre_height = (block_height - text_height)//2 #Text centering
        textRect = pygame.Rect(rect[0] + centre_width, rect[1] + centre_height, text_width, text_height)
        screen.blit(text, textRect)

        if back_Rect.collidepoint(mouseX, mouseY):
            if button == 1: 
                menuScreen()

        headerTitle = titleFont.render("HOW TO PLAY", False, WHITE)
        infoTitle = font.render("Use left, right & down arrow keys to move block pieces.", False, WHITE)
        infoTitle2 = font.render("Use the Up arrow key to rotate your current block piece.", False, WHITE)
        infoTitle3 = smallFont.render("Clear horizontal lines of blocks to score points, & Remember not to hit the top!", False, WHITE)
        
        headerRect = headerTitle.get_rect()
        infoRect = infoTitle.get_rect()
        infoRect2 = infoTitle2.get_rect()
        infoRect3 = infoTitle3.get_rect()

        headerRect.center = (centreX, 180)
        infoRect.center = (centreX, 240)
        infoRect2.center = (centreX, 300)
        infoRect3.center = (centreX, 340)

        screen.blit(headerTitle, headerRect)
        screen.blit(infoTitle, infoRect)
        screen.blit(infoTitle2, infoRect2)
        screen.blit(infoTitle3, infoRect3)

        pygame.display.update()

    pygame.quit()

#Main menu Function
def menuScreen(): 
    running = True
    #button state
    button = 0
    #mouse Position
    mouseX = 0
    mouseY = 0

    while running:
        win.fill(BLACK) #Window screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                button = event.button

            if event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos

        buttonList = [game_Rect, help_Rect]
        optionList = [mainGame, instructions]
        namesList = ["Play", "Instructions"]  
        pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height))

        for i in range(len(buttonList)):
            rect = buttonList[i] #get buttonLists
            pygame.draw.rect(screen, WHITE, rect)
            text = font.render(namesList[i], True, BLACK)
            text_width, text_height = font.size(namesList[i])
            centre_width = (block_width - text_width)//2 #Text centering
            centre_height = (block_height - text_height)//2 #Text centering
            textRect = pygame.Rect(rect[0] + centre_width, rect[1] + centre_height, text_width, text_height)
            screen.blit(text, textRect)

        #Start Game
        if game_Rect.collidepoint(mouseX, mouseY):
            if button == 1: 
                mainGame() 

        #View instructions
        if help_Rect.collidepoint(mouseX, mouseY):
            if button == 1: 
                instructions() 
        
        #Title
        gameTitle = titleFont.render("TETRIS", False, WHITE)
        gameRect = gameTitle.get_rect()
        gameRect.center = (centreX, 200)
        win.blit(gameTitle, gameRect)
        
        pygame.display.update()
    
    pygame.quit()
 
 
win = pygame.display.set_mode((screen_width, screen_height)) #display screen background
menuScreen()  # start program (main menu)
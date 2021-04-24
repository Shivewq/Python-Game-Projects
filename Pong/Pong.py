import pygame, random

#Setup Game Code
def ball_movement():
   #Move the ball
   global speed, ballspeedX, ballspeedY, paddleBScore, paddleAScore, scoreTime
   ball.x += ballspeedX
   ball.y += ballspeedY
   # check for collision with walls
   if ball.top <= 0 or ball.bottom >= screenHeight: #Will multiply speed by -1 at collision (vertically) 
      ballspeedY *= -1
   if ball.left <= 0:
     scoreTime = pygame.time.get_ticks()
     paddleBScore += 1
   if ball.right >= screenWidth: #will multiply x speed by -1 at collision (horizontally)
     scoreTime = pygame.time.get_ticks()
     paddleAScore += 1
   # check for collision with paddles
   if ball.colliderect(paddleA) and ballspeedX < 0:
    #Collision with paddleA. Paddle & ball speed increases on hit
     if abs(ball.left - paddleA.right) < 30: #Position of ball left side & paddleA right side less than 30:
     #Reverse ball direction & speed up
       ballspeedX *= -1.12
       ballspeedY *= 1.11
       speed *= 1.1 
     elif abs(ball.bottom - paddleA.top) < 50 and ballspeedY > 0: #collision with top/bottom of paddle ( prevents it clipping through the paddle)
       ballspeedY *= -1
     elif abs(ball.top - paddleA.bottom) < 50 and ballspeedY < 0:
       ballspeedY *= -1
   #Collision with paddleB. Paddle & ball speed increases on hit
   if ball.colliderect(paddleB) and ballspeedX > 0:
     if abs(ball.right - paddleB.left) > 10: #Position of ball right & paddleB left greater than 10:
     #Reverse ball direction & speed up
       ballspeedX *= -1.12
       ballspeedY *= 1.11
       speed *= 1.1
     elif abs(ball.bottom - paddleB.top) < 10 and ballspeedY > 0: #collision with top/bottom of paddle
       ballspeedY *= -1
     elif abs(ball.top - paddleB.bottom) < 10 and ballspeedY < 0:
       ballspeedY *= -1

#Menu Simulation
def ball_menu():
   #Move the ball
   global ballspeedX, ballspeedY
   ball.x += ballspeedX
   ball.y += ballspeedY
   # check for collision with walls (reverse speed vertically and horizontally by -1)
   if ball.top <= 0 or ball.bottom >= screenHeight: 
      ballspeedY *= -1
   if ball.left <= 0 or ball.right >= screenWidth: 
      ballspeedX *= -1

#Paddle Movement
def player_movement():
  #Old y-Positions of paddles
    global oldBy, oldAy
    oldAy =  paddleA.y
    oldBy = paddleB.y

    #Paddle movement  
    paddleA.move_ip(0,paddleAy)
    
    #Collision detection with Wall
    if paddleA.y <= 0 or paddleA.y >= screenHeight - height:
        paddleA.y = oldAy

#Opponent A.I movement 
def opponent_AI():
  if paddleB.top < ball.y:
      paddleB.top += speed 
  if paddleB.top > ball.y:
      paddleB.top -= speed + 0.15
  #Collision detection with Wall
  if paddleB.y <= 0 or paddleB.y >= screenHeight - height:
      paddleB.y = oldBy

#Reset the ball back to middle after score
def ball_reset():
  global ballspeedY, ballspeedX, speed, scoreTime
  #Tracks game time
  currentTime = pygame.time.get_ticks()
  ball.center = (centreX, centreY)
  speed = 4.5 #Reset Player's speed on ball reset
  #Countdown before new ball moves
  if currentTime - scoreTime < 700: # count from 3 within 700 ticks
    count3 = scoreFont.render("3", False, WHITE)
    screen.blit(count3,(centreX - 6, centreY - 50))
  if 700 < currentTime - scoreTime < 1400: #display 2 within 700-1400 ticks
    count2 = scoreFont.render("2", False, WHITE)
    screen.blit(count2,(centreX - 6, centreY - 50))
  if 1400 < currentTime - scoreTime < 2100: #display 1 within 1400-2100 ticks
    count1 = scoreFont.render("1", False, WHITE)
    screen.blit(count1,(centreX - 6, centreY - 50))

  if currentTime - scoreTime < 2100:
   ballspeedY, ballspeedX = 0,0
  else:
    ballspeedY = 4.5 * random.choice((-1,1)) #Goes Right, up or down randomly (reverse speed by -1)
    ballspeedX = 4.5 
    scoreTime = None

#Resets score back to 0 upon call (called in final screens)
def score_reset():
  global paddleAScore, paddleBScore
  paddleAScore = 0
  paddleBScore = 0


# Setup screen
pygame.init()
#Clock setup
clock = pygame.time.Clock()
FPS = 60
SIZE = (800,600)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pong")

#Centre of screen
screenWidth = screen.get_width()
screenHeight = screen.get_height()
centreX = screenWidth / 2
centreY = screenHeight / 2

# Colours to use throughout
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (44, 58, 71)
LIME = (0, 128, 0)
ORANGE = (255,100,10)
SMOKEWHITE = (202, 211, 200)

# Set up fonts to use
fontTitle = pygame.font.SysFont("dejavusansmono",35,bold = True)
fontTitleBold = pygame.font.SysFont("dejavusansmono",25, bold = True)
fontInfo = pygame.font.SysFont("dejavusansmono", 15, italic = True) 
scoreFont = pygame.font.SysFont("dejavusansmono",24,bold = True)

# Initialize paddles & ball
#starting positions
aX = 10
bX = 780
aY = 240
bY = 240

#y-pos modifier for key press detection
paddleAy = 0

#Shape of paddles
height = 120
width = 10

#Assign Rects
#Paddles
paddleA = pygame.Rect(aX, aY, width, height)
paddleB = pygame.Rect(bX, bY, width, height)
#Ball
ball = pygame.Rect(centreX , centreY ,16, 16)

#Move Speed
speed = 4.5

#Score 
paddleAScore = 0
paddleBScore = 0

#Ball speed
ballspeedY = 4.5
ballspeedX = 4.5

#mouse Position
mouseX = 0
mouseY = 0

#Button Rects for Menu
blockWidth = screenWidth // 3
blockHeight = screenHeight // 7

playRect = pygame.Rect(blockWidth, blockHeight, blockWidth, blockHeight)
helpRect = pygame.Rect(blockWidth, 4*blockHeight, blockWidth, blockHeight)

# Initialize the game Loop
running = True
menu = True
game = False
instructions = False
WinScreen = False
LoseScreen = False
#Score Timer
scoreTime = True

screen.fill(GRAY)

# Main loop
while running:
  button = 0
  # check for any events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      # end the program if x clicked
      running = False
  
  # intro Loop
  while menu:

    screen.fill(GRAY)

    # check for some events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        menu = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouseX, mouseY = event.pos
        button = event.button
      if event.type == pygame.MOUSEMOTION:
        mouseX, mouseY = event.pos
    buttonList = [playRect, helpRect]
    optionList = [game, instructions]
    nameList = ["Play", "Instructions"]  
    pygame.draw.rect(screen, GRAY, (0, 0, screenWidth, screenHeight))

    for i in range(len(buttonList)):
      rect = buttonList[i] #get Rects
      pygame.draw.rect(screen, SMOKEWHITE, rect) 
      text = fontTitle.render(nameList[i], True, BLACK) #render Font text
      textWidth, textHeight = fontTitle.size(nameList[i]) #Text sizing
      centreW = (blockWidth - textWidth)//2  #Centering
      centreH = (blockHeight - textHeight)//2
      textRect = pygame.Rect(rect[0] + centreW, rect[1] + centreH, textWidth, textHeight)
      screen.blit(text, textRect)

    if playRect.collidepoint(mouseX, mouseY): #Normal mode: normal sized paddles - easier to score
      pygame.draw.rect(screen, BLACK, playRect, 5)
      if button == 1:
        game = True
        menu = False
    elif helpRect.collidepoint(mouseX, mouseY):
      pygame.draw.rect(screen, BLACK, helpRect, 5)
      if button == 1:
        instructions = True
        menu = False
 
          
    #Menu Title
    textTitle = fontTitle.render("Pong!!!", False, SMOKEWHITE)
    textRect = textTitle.get_rect()
    textRect.center = (centreX, 250)
    screen.blit(textTitle,textRect)
   
    pygame.draw.ellipse(screen, WHITE, ball)
    ball_menu()
  
    pygame.display.update()

  # Instruction loop containing information for user
  while instructions:
    screen.fill(GRAY)
    # check for key press
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
         instructions = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p:
          instructions = False
          game = True
    # Have text for instuctions of game and how to go back or play game
    headerTitle = fontTitle.render("RULES & CONTROLS:", False, ORANGE)
    infoTitle = fontInfo.render("Left Paddle: W & S keys | Left Paddle is A.I", False, WHITE)
    infoTitle2 = fontInfo.render("Score points by successfully hitting the AI opponent's wall! First to get 6 points wins.", False, WHITE)
    infoTitle3 = fontInfo.render("Paddle speed & ball speed increase on impact during each round!", False, WHITE)
    infoTitle4 = fontInfo.render("Press P to continue.", False, WHITE)
    #Rects for Text
    headerRect = headerTitle.get_rect()
    infoRect = infoTitle.get_rect()
    infoRect2 = infoTitle2.get_rect()
    infoRect3 = infoTitle3.get_rect()
    infoRect4 = infoTitle4.get_rect()
    #Position Rects
    headerRect.center = (centreX, 180) 
    infoRect.center = (centreX, 240)
    infoRect2.center = (centreX, 280)
    infoRect3.center = (centreX, 320)
    infoRect4.center = (centreX, 360)

    screen.blit(headerTitle, headerRect)
    screen.blit(infoTitle, infoRect)
    screen.blit(infoTitle2, infoRect2)
    screen.blit(infoTitle3, infoRect3)
    screen.blit(infoTitle4, infoRect4)

    pygame.display.update()

  # All Gameplay Loop
  while game:
    screen.fill(GRAY)
    #Check key events
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # If user clicked close (X)
          running = False # Flag as done to exit this loop
        if event.type == pygame.KEYDOWN:   
         # Move the paddles
          if event.key == pygame.K_w:
           paddleAy -= speed
          if event.key == pygame.K_s:
           paddleAy += speed
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_w or event.key == pygame.K_s:
            paddleAy = 0

    #Track score goal to Win/Lose Loop
    if paddleAScore == 6:
      game = False
      WinScreen = True
    elif paddleBScore == 6:
      game = False
      LoseScreen = True

    #When scoreTime is true, only then reset the ball (to sync with timer)
    if scoreTime:
      ball_reset()
    
    #Draw Game Assets (paddles, ball, Score, Net)
    #paddles
    pygame.draw.rect(screen, SMOKEWHITE, paddleA, 0)
    pygame.draw.rect(screen, SMOKEWHITE, paddleB, 0)
    #ball
    pygame.draw.ellipse(screen, WHITE, ball)
    #Net
    pygame.draw.line(screen, WHITE, (centreX,0), (centreX, 800), 1)
    
    #Main game code (Paddle/ball movements)
    ball_movement()
    player_movement()
    opponent_AI()
    
    # score counter - text that gets updated
    scoreA = scoreFont.render(f"{paddleAScore}", False, SMOKEWHITE) # f-strings, which formats different values based on expressions given
    screen.blit(scoreA,(centreX - 25,centreY))
    scoreB = scoreFont.render(f"{paddleBScore}", False, SMOKEWHITE)
    screen.blit(scoreB,(centreX + 12,centreY))
    
    #update game graphics/movement
    pygame.display.update()
    #FPS cap
    clock.tick(80)
    
  #Final loop (if player (paddleA) Wins)
  while WinScreen:
    screen.fill(BLACK)
    # check for key events
    for event in pygame.event.get(): 
       if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_p: #Pressing the p Key will replay the game
            score_reset() #Resets previous scores back to 0
            game = True
            WinScreen = False
    #Create Win Text
    winText = fontTitle.render("YOU WIN! Press P to play again!", False, LIME)
    winRect = winText.get_rect() #Create Rect for text
    winRect.center = (centreX, centreY) #Rect positioning (centered)
    screen.blit(winText, winRect) #Merge Text & Rect

    pygame.display.update()
  
  #Final loop (if A.I (paddleB) Wins)
  while LoseScreen:
    screen.fill(BLACK)
    # check for key events
    for event in pygame.event.get(): 
       if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_p: #Pressing the p Key will replay the game
            score_reset()
            game = True
            LoseScreen = False
    #Create Text
    loseText = fontTitle.render("YOU LOSE! AI WINS!", False, LIME)
    retryText = fontTitle.render("P - Try again? | Q - Quit?", False, LIME)
    #Create Rects
    loseRect = loseText.get_rect()
    retryRect = retryText.get_rect()
    #Rect positioning
    loseRect.center = (centreX, centreY) #Centered
    retryRect.center = (centreX, 300)
    #Merge Text & Rect
    screen.blit(loseText, loseRect)
    screen.blit(retryText, retryRect)

    #update game graphics & movements
    pygame.display.update()
  
    #update game graphics & movements
  pygame.display.update()
    #FPS cap/limit her second
  clock.tick(60)

pygame.quit()
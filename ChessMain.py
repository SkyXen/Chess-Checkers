import pygame as p
import ChessEngine, SmartMove

WIDTH = HEIGHT = 512
DIMENSION = 8 # 8*8 Chess board
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 # for animation
IMAGES = {}


def loadImages():
  pieces = ['wP', 'wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
  for piece in pieces:
    IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

  #can be accessed using IMAGES['wP']


def main():
  p.init()
  screen = p.display.set_mode((WIDTH,HEIGHT))
  clock = p.time.Clock()
  screen.fill(p.Color("white"))
  gs = ChessEngine.GameState()
  validMoves = gs.getValidMoves()
  moveMade = False
  loadImages()
  running = True
  sqSelected = () #atpresent no square selected, keep track of last clicked square (tuple:(row,col))
  playerClicks = [] #keep track of player clicks(two tuples: [(6,4),(4,4)])
  gameOver = False
  playerOne = False #If a human is playing white then this is true || if AI is playing black then this is true
  playerTwo = True #If AI is playing white then this is true || if human is playing black then this is true
  numberOfChecksWhite = 3
  numberOfChecksBlack = 3

  while running:
    humanTurn  = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

    for e in p.event.get():
      if e.type == p.quit:
        running = False

      #mousehandler
      elif e.type == p.MOUSEBUTTONDOWN:
        if not gameOver and humanTurn:
          location = p.mouse.get_pos() #(x,y) location of mouse
          col = location[0]//SQ_SIZE
          row = location[1]//SQ_SIZE
          if sqSelected == (row,col): #Already selected square
            sqSelected = () #Unselect it
            playerClicks = [] #clear it
          else:
            sqSelected = (row,col) #if not already selected then select it
            playerClicks.append(sqSelected)
          if len(playerClicks) == 2:
            move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)

            print(move.getChessNotation(), numberOfChecksBlack, numberOfChecksWhite)
            for i in range(len(validMoves)):
              if move == validMoves[i]:
                gs.makeMove(validMoves[i])
                if gs.inCheck():
                  if gs.whiteToMove:
                    numberOfChecksWhite -= 1
                  else:
                    numberOfChecksBlack -= 1
                moveMade = True
                sqSelected = () #reset user clicks
                playerClicks = []
            if not moveMade:
              playerClicks = [sqSelected]

      #key_handler
      elif e.type == p.KEYDOWN:
        if e.key == p.K_z:
          gs.undoMove()
          moveMade = True
          gameOver = False

        if e.key == p.K_r:
          gs = ChessEngine.GameState()
          validMoves = gs.getValidMoves()
          sqSelected = ()
          playerClicks = []
          moveMade = False
          gameOver = False
          numberOfChecksBlack = 3
          numberOfChecksWhite = 3

    ##AI MOVES##
    if not gameOver and not humanTurn:
      AIMove = SmartMove.findBestMove(gs,validMoves, numberOfChecksWhite, numberOfChecksBlack)
      if AIMove is None:
        AIMove = SmartMove.findRandomMove(validMoves)
      gs.makeMove(AIMove)
      if gs.inCheck():
        if gs.whiteToMove:
          numberOfChecksWhite -= 1
        else:
          numberOfChecksBlack -= 1
      print(AIMove.getChessNotation(), numberOfChecksBlack, numberOfChecksWhite)

      moveMade = True


    if moveMade:
      validMoves = gs.getValidMoves()
      moveMade = False

    drawGameState(screen, gs, validMoves, sqSelected)

    if gs.whiteToMove and gs.inCheck() and numberOfChecksWhite == 0:
      gameOver = True
      drawText(screen, "Black wins by ThreeChecks")

    else:
      if gs.inCheck() and numberOfChecksBlack == 0:
        gameOver = True
        drawText(screen, "White wins by ThreeChecks")


    if gs.checkMate or gs.staleMate:
      gameOver = True
      drawText(screen, "STALEMATE" if gs.staleMate else "Black wins by CHECKMATE" if gs.whiteToMove else "White wins by CHECKMATE")

    clock.tick(MAX_FPS)
    p.display.flip()

  print(gs.board)



def drawGameState(screen,gs,validMoves,sqSelected):
  drawBoard(screen)#draw squares on board
  highlightSquares(screen,gs,validMoves,sqSelected)
  drawPieces(screen, gs.board) #draw pieces on board



def drawBoard(screen):
  colors = [p.Color("white"), p.Color("gray")]
  for r in range(DIMENSION):
    for c in range(DIMENSION):
      color = colors[((r + c) % 2)]
      p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, gs, validMoves, sqSelected):
  if sqSelected != ():
    r, c = sqSelected
    if gs.board[r][c][0] ==("w" if gs.whiteToMove else "b"):
      #highlight selected square
      s = p.Surface((SQ_SIZE,SQ_SIZE))
      s.set_alpha(100)
      s.fill(p.Color("blue"))
      screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))

      #highlight move around the selectd square
      s.fill(p.Color("green"))
      for move in validMoves:
        if move.startRow == r and move.startCol == c:
          screen.blit(s,(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

      s.fill(p.Color("red"))
      if gs.inCheck() == True and gs.board[r][c][0] == "w":
        r,c = gs.whiteKingLocation
        screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
      if gs.inCheck() == True and gs.board[r][c][0] == "b":
        r,c = gs.blackKingLocation
        screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))



#draw pieces on board using current game state
def drawPieces(screen,board):
  for r in range(DIMENSION):
    for c in range(DIMENSION):
      piece = board[r][c]
      if piece != "--":
        screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawText(screen, text):
  font = p.font.SysFont("Helvitca", 32,True,False)
  textObject = font.render(text,0,p.Color("Black"))
  textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
  screen.blit(textObject, textLocation)

def drawEndGameText(screen,text):
  pass

if __name__ == "__main__":
  main()
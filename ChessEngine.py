
class GameState():

  def __init__(self):
    self.board = [
        ["bR","bN","bB","bQ","bK","bB","bN","bR"],
        ["bP","bP","bP","bP","bP","bP","bP","bP"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["wP","wP","wP","wP","wP","wP","wP","wP"],
        ["wR","wN","wB","wQ","wK","wB","wN","wR"]]

    self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                          'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K':self.getKingMoves}

    self.whiteToMove = True
    self.moveLog = []
    self.moveCount = 0
    self.whiteKingLocation = (7,4)
    self.blackKingLocation = (0,4)
    self.checkMate = False
    self.staleMate = False

  def makeMove(self,move):
    self.board[move.startRow][move.startCol] = "--"
    self.board[move.endRow][move.endCol] = move.pieceMoved
    self.moveLog.append(move) #save the log of moved pieces
    self.moveCount += 1
    self.whiteToMove = not self.whiteToMove #swap players
    #update King's location
    if move.pieceMoved == "wK":
      self.whiteKingLocation = (move.endRow, move.endCol)

    elif move.pieceMoved == "bK":
      self.blackKingLocation = (move.endRow, move.endCol)


  #undo the above moves
  def undoMove(self):
    if len(self.moveLog) != 0:
      move = self.moveLog.pop()
      self.moveCount -= 1
      self.board[move.startRow][move.startCol] = move.pieceMoved
      self.board[move.endRow][move.endCol] = move.pieceCaptured
      self.whiteToMove = not self.whiteToMove
      #update King's location
      if move.pieceMoved == "wK":
        self.whiteKingLocation = (move.startRow, move.startCol)

      elif move.pieceMoved == "bK":
        self.blackKingLocation = (move.startRow, move.startCol)

      self.checkMate = False
      self.staleMate = False

  def getValidMoves(self):
    moves = self.getAllPossibleMoves()
    for i in range(len(moves)-1,-1,-1):
      self.makeMove(moves[i])
      self.whiteToMove = not self.whiteToMove
      #checking if the king is in check or not
      if self.inCheck():
        moves.remove(moves[i])
      self.whiteToMove = not self.whiteToMove
      self.undoMove()

    if len(moves) == 0:
      if self.inCheck():
        self.checkMate = True
      else:
        self.staleMate = True
    else:
      self.checkMate = False
      self.staleMate = False

    return moves

  def inCheck(self):
    if self.whiteToMove:
      return self.sqUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
    else:
      return self.sqUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


  def sqUnderAttack(self,r,c):
    self.whiteToMove = not self.whiteToMove #switch to opp's turn
    oppMoves = self.getAllPossibleMoves()
    self.whiteToMove = not self.whiteToMove #switch back
    for move in oppMoves:
      if move.endRow == r and move.endCol == c:
        return True
    return False



  def getAllPossibleMoves(self):
    moves = []
    for r in range(len(self.board)):
      for c in range(len(self.board[r])):
        turn = self.board[r][c][0]
        if( turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
          piece = self.board[r][c][1]
          self.moveFunctions[piece](r,c,moves)

    return moves

  #get all pawn moves at r,c and add to moves list
  def getPawnMoves(self,r,c,moves):
    if self.whiteToMove: #white pieces move
      #Moving pieces
      if c-1 >= 0:
        if self.board[r-1][c-1] == "--":
          moves.append(Move((r,c),(r-1,c-1),self.board))

      if c+1 <= 7:
        if self.board[r-1][c+1] == "--":
          moves.append(Move((r,c),(r-1,c+1),self.board))

      if self.board[r-1][c][0] == 'b':    #capturing forward piece
        moves.append(Move((r,c),(r-1,c),self.board))

    else: #black piece move
      #Moving pieces
      if r+1<=7:
        if c-1 >= 0:
          if self.board[r+1][c-1] == "--":
            moves.append(Move((r,c),(r+1,c-1),self.board))

        if c+1 <= 7:
          if self.board[r+1][c+1] == "--":
            moves.append(Move((r,c),(r+1,c+1),self.board))

        if c>=0 and c<=7:
          if self.board[r+1][c][0] == 'w':    #capturing forward piece
            moves.append(Move((r,c),(r+1,c),self.board))



  def getRookMoves(self,r,c,moves):
    directions = ((-1,0),(0,-1),(1,0),(0,1)) #up, left, down, right
    enemyColor = "b" if self.whiteToMove else "w"
    for d in directions:
      for i in range(1,8):
        endRow = r + d[0] * i
        endCol = c + d[1] * i

        if 0 <= endRow < 8 and 0<= endCol<8:
          endPiece = self.board[endRow][endCol]
          if endPiece == "--":
            moves.append(Move((r,c), (endRow,endCol), self.board))
          elif endPiece[0] == enemyColor:
            moves.append(Move((r,c), (endRow,endCol), self.board))
            break
          else:
            break
        else:
          break


  def getKnightMoves(self,r,c,moves):
    knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
    allyColor = "w" if self.whiteToMove else "b"
    for m in knightMoves:
      endRow = r + m[0]
      endCol = c + m[1]

      if 0<= endRow <8 and 0<=endCol<8:
        endPiece = self.board[endRow][endCol]
        if endPiece[0] != allyColor:
          moves.append(Move((r,c),(endRow, endCol), self.board))

  def getBishopMoves(self,r,c,moves):
    directions = ((-1,-1),(-1,1),(1,-1),(1,1)) #diagonals
    enemyColor = "b" if self.whiteToMove else "w"
    for d in directions:
      for i in range(1,8):
        endRow = r + d[0] * i
        endCol = c + d[1] * i

        if 0 <= endRow < 8 and 0<= endCol<8:
          endPiece = self.board[endRow][endCol]
          if endPiece == "--":
            moves.append(Move((r,c), (endRow,endCol), self.board))
          elif endPiece[0] == enemyColor:
            moves.append(Move((r,c), (endRow,endCol), self.board))
            break
          else:
            break
        else:
          break

  def getKingMoves(self,r,c,moves):
    kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
    allyColor = "w" if self.whiteToMove else "b"

    for i in range(8):
      endRow = r + kingMoves[i][0]
      endCol = c + kingMoves[i][1]
      if 0<=endRow<8 and 0<=endCol<8:
        endPiece = self.board[endRow][endCol]
        if endPiece[0] != allyColor:
          moves.append(Move((r,c),(endRow,endCol),self.board))


  def getQueenMoves(self,r,c,moves):
    self.getRookMoves(r,c,moves)
    self.getBishopMoves(r,c,moves)




class Move():
  ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
  rowsToRanks = {v: k for k, v in ranksToRows.items()}

  filesToCols = {"a":0, "b":1, "c":2, "d":3,
                   "e":4, "f":5, "g":6, "h":7}
  colsToFiles = {v: k for k, v in filesToCols.items()}

  def __init__(self, startSq, endSq, board):


    self.startRow = startSq[0]
    self.startCol = startSq[1]
    self.endRow = endSq[0]
    self.endCol = endSq[1]
    self.pieceMoved = board[self.startRow][self.startCol]
    self.pieceCaptured = board[self.endRow][self.endCol]
    self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow *10 + self.endCol


  #overriding the equals method
  def __eq__(self, other):
    if isinstance(other,Move):
      return self.moveID == other.moveID
    return False

  def getChessNotation(self):
    #can be added to make this like real chess notation
    return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


  def getRankFile(self, r, c):
    return self.colsToFiles[c] + self.rowsToRanks[r]

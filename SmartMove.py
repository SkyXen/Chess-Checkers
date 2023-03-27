import random
 

pieceScore = { "K": 0, "Q": 10, "R":5, "B":3, "N":3, "P":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

def findBestMove(gs, validMoves):
    trunMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                if gs.checkMate:
                    score = -trunMultiplier * CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -trunMultiplier * scoreMaterial(gs.board)
                opponentMaxScore = max(opponentMaxScore, score)
                gs.undoMove()

        if  opponentMaxScore < opponentMinMaxScore :
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

##Helper METHOD to make first recursive call##
def findBestMinMaxMove(gs, validMoves):
    global nextMove
    nextMove = None
    minMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove

def minMax(gs, validMoves, depth, whiteToMove):
    #global nextMove
    #if depth == 0
    #return scoreMaterial(gs.board)
    pass


def scoreBoard(gs):
    pass

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]


    return score

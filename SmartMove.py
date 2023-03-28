import random
 

pieceScore = { "K": 0, "Q": 10, "R":5, "B":3, "N":3, "P":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

# def findBestMove(gs, validMoves):
#     trunMultiplier = 1 if gs.whiteToMove else -1
#     opponentMinMaxScore = CHECKMATE
#     bestPlayerMove = None
#     random.shuffle(validMoves)
#     for playerMove in validMoves:
#         gs.makeMove(playerMove)
#         opponentMoves = gs.getValidMoves()
#         if gs.staleMate:
#             opponentMaxScore = STALEMATE
#         elif gs.checkMate:
#             opponentMaxScore = -CHECKMATE
#         else:
#             opponentMaxScore = -CHECKMATE
#             for opponentMove in opponentMoves:
#                 gs.makeMove(opponentMove)
#                 if gs.checkMate:
#                     score = -trunMultiplier * CHECKMATE
#                 elif gs.staleMate:
#                     score = STALEMATE
#                 else:
#                     score = -trunMultiplier * scoreMaterial(gs.board)
#                 opponentMaxScore = max(opponentMaxScore, score)
#                 gs.undoMove()

#         if  opponentMaxScore < opponentMinMaxScore :
#             opponentMinMaxScore = opponentMaxScore
#             bestPlayerMove = playerMove
#         gs.undoMove()
#     return bestPlayerMove

##Helper METHOD to make first recursive call##
def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    moveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove

def minMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = minMax(gs, nextMoves, depth-1, False)
            if score>maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = minMax(gs, nextMoves, depth-1, True)
            if score< minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def moveNegaMax(gs,validMoves,depth,turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -moveNegaMax(gs,nextMoves,depth-1,-turnMultiplier)
        if score>maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove=move
        gs.undoMove()
    return maxScore

def moveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -moveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier)
        if score>maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove=move
        gs.undoMove()
        if maxScore > alpha: #pruning
            alpha = maxScore
        if alpha >=beta:
            break
    return maxScore

##A positive score is good for white, a negative score is good for black

def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif gs.staleMate:
        return STALEMATE
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]


    return score

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]


    return score

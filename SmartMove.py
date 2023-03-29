import random


pieceScore = { "K": 0, "Q": 10, "R":5, "B":3, "N":3, "P":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
CHECKMATEDEPTH = 3

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
    # random.shuffle(validMoves)
    moveNegaMax2(gs, validMoves, 1 if gs.whiteToMove else -1, CHECKMATEDEPTH)
    # moveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
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

def checkCondition(gs):
    return CHECKMATE if gs.incheck() else -CHECKMATE

def moveNegaMax2(gs,validMoves,turnMultiplier,checkmateDepth):
    global nextMove
    queue = []
    score = 0
    maxScore = 0
    for i in validMoves:
        queue.append(([i], 1))
    # print(queue)
    while queue:
        move = queue.pop(0)
        print(move[1])
        if (move[1] > checkmateDepth): break
        for i in range(0, move[1]):
            gs.makeMove(move[0][i])
        if gs.whiteToMove:
            if gs.inCheck():
                for i in range(0, move[1]):
                    gs.undoMove()
                continue
            else:
                for i in gs.getValidMoves():
                    temp = move[0].copy()
                    temp.append(i)
                    queue.append((temp, move[1] + 1))
        else:
            if gs.inCheck():
                nextMove = move[0][0]
                for i in range(0, move[1]):
                    gs.undoMove()
                return
            else:
                for i in gs.getValidMoves():
                    temp = move[0].copy()
                    temp.append(i)
                    queue.append((temp, move[1] + 1))
        for i in range(0, move[1]):
            gs.undoMove()
    return moveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, turnMultiplier)

##A positive score is good for white, a negative score is good for black

def scoreBoard(gs):

    if gs.inCheck():
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
                score += 0 * pieceScore[square[1]]
            elif square[0] == "b":
                score -= 0 * pieceScore[square[1]]


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

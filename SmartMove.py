import random


pieceScore = { "K": 0, "Q": 10, "R":5, "B":3, "N":3, "P":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 1
CHECKMATEDEPTH = 10

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

def checkCondition(gs, turnMultiplier):
    score = 0
    if gs.inCheck():
        if gs.whiteToMove:
            score = turnMultiplier * -CHECKMATE #black wins
        else:
            score = turnMultiplier * CHECKMATE #white wins
    return score

def moveNegaMax2(gs,validMoves,turnMultiplier, checkmateDepth):
    global nextMove
    queue = []
    score = 0
    maxScore = 0
    for i in validMoves:
        queue.append(([i], 1))
    # print(queue)
    while queue:
        move = queue.pop(0)
        turnMultiplier = turnMultiplier * (-1 if (move[1] % 2 == 0) else 1)
        # print(move)
        for i in range(0, move[1]):
            gs.makeMove(move[0][i])
        nextMoves = gs.getValidMoves()
        score = checkCondition(gs, turnMultiplier)
        if score == CHECKMATE:
            maxScore = score
            nextMove = move[0][0]
            for i in range(0, move[1]):
                gs.undoMove()
            return maxScore
        minscore = 0
        maxscore = 0
        for moves in nextMoves:
            gs.makeMove(moves)
            minscore = min(minscore, checkCondition(gs, turnMultiplier))
            maxscore = max(maxscore, checkCondition(gs, turnMultiplier))
            gs.undoMove()
        if minscore == -CHECKMATE:
            for i in range(0, move[1]):
                gs.undoMove()
            continue
        elif minscore == 0 and maxscore == CHECKMATE:
            maxScore = score
            nextMove = move[0][0]
            for i in range(0, move[1]):
                gs.undoMove()
            return maxScore
        else:
            for moves in nextMoves:
                temp = move[0].copy()
                temp.append(moves)
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

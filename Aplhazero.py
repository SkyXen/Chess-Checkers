import numpy as np
import ChessEngine

def encode_board(board):
    board_state = board.board;
    encoded = np.zeros([8,8,14]).astype(int)
    encoder_dict = {"bR":0, "bN":1, "bB":2, "bQ":3, "bK":4, "bP":5, "wR":6, "wN":7, "wB":8, "wQ":9, "wK":10, "--":11}
    for i in range(8):
        for j in range(8):
            if board_state[i,j] != "--":
                encoded[i,j,encoder_dict[board_state[i,j]]] = 1
    if board.whiteToMove:
        encoded[:,:,12] = 1 # player to move
    # if board.K_move_count != 0:
    #         encoded[:,:,13] = 1 # cannot castle queenside for white
    #         encoded[:,:,14] = 1 # cannot castle kingside for white
    # if board.K_move_count == 0 and board.R1_move_count != 0:
    #         encoded[:,:,13] = 1
    # if board.K_move_count == 0 and board.R2_move_count != 0:
    #         encoded[:,:,14] = 1
    # if board.k_move_count != 0:
    #         encoded[:,:,15] = 1 # cannot castle queenside for black
    #         encoded[:,:,16] = 1 # cannot castle kingside for black
    # if board.k_move_count == 0 and board.r1_move_count != 0:
    #         encoded[:,:,15] = 1
    # if board.k_move_count == 0 and board.r2_move_count != 0:
    #         encoded[:,:,16] = 1
    encoded[:,:,13] = board.moveCount
    # encoded[:,:,18] = board.repetitions_w
    # encoded[:,:,19] = board.repetitions_b
    # encoded[:,:,20] = board.no_progress_count
    # encoded[:,:,21] = board.en_passant
    return encoded

def decode_board(encoded):
    decoded = ChessEngine.GameState()
    decoded.board[:,:] = "--"
    decoder_dict = {0:"bR", 1:"bN", 2:"bB", 3:"bQ", 4:"bK", 5:"bP", 6:"wR", 7:"wN", 8:"wB", 9:"wQ", 10:"wK", 11:"wP"}
    for i in range(8):
        for j in range(8):
            for k in range(12):
                if encoded[i,j,k] == 1:
                    decoded.board[i,j] = decoder_dict[k]
    # board.current_board = decoded
    if encoded[0,0,12] == 0:
        decoded.whiteToMove = False
    # if encoded[0,0,13] == 1:
    #     board.R1_move_count = 1
    # if encoded[0,0,14] == 1:
    #     board.R2_move_count = 1
    # if encoded[0,0,15] == 1:
    #     board.r1_move_count = 1
    # if encoded[0,0,16] == 1:
    #     board.r2_move_count = 1
    decoded.moveCount = encoded[0,0,17]
    # board.repetitions_w = encoded[0,0,18]
    # board.repetitions_b = encoded[0,0,19]
    # board.no_progress_count = encoded[0,0,20]
    # board.en_passant = encoded[0,0,21]
    return decoded

def encode_action(board,initial_pos,final_pos,underpromote=None):
    encoded = np.zeros([8,8,73]).astype(int)
    i, j = initial_pos; x, y = final_pos; dx, dy = x-i, y-j
    piece = board.current_board[i,j]
    if piece in ["R","B","Q","K","P","r","b","q","k","p"] and underpromote in [None,"queen"]: # queen-like moves
        if dx != 0 and dy == 0: # north-south idx 0-13
            if dx < 0:
                idx = 7 + dx
            elif dx > 0:
                idx = 6 + dx
        if dx == 0 and dy != 0: # east-west idx 14-27
            if dy < 0:
                idx = 21 + dy
            elif dy > 0:
                idx = 20 + dy
        if dx == dy: # NW-SE idx 28-41
            if dx < 0:
                idx = 35 + dx
            if dx > 0:
                idx = 34 + dx
        if dx == -dy: # NE-SW idx 42-55
            if dx < 0:
                idx = 49 + dx
            if dx > 0:
                idx = 48 + dx
    if piece in ["n","N"]: # Knight moves 56-63
        if (x,y) == (i+2,j-1):
            idx = 56
        elif (x,y) == (i+2,j+1):
            idx = 57
        elif (x,y) == (i+1,j-2):
            idx = 58
        elif (x,y) == (i-1,j-2):
            idx = 59
        elif (x,y) == (i-2,j+1):
            idx = 60
        elif (x,y) == (i-2,j-1):
            idx = 61
        elif (x,y) == (i-1,j+2):
            idx = 62
        elif (x,y) == (i+1,j+2):
            idx = 63
    if piece in ["p", "P"] and (x == 0 or x == 7) and underpromote != None: # underpromotions
        if abs(dx) == 1 and dy == 0:
            if underpromote == "rook":
                idx = 64
            if underpromote == "knight":
                idx = 65
            if underpromote == "bishop":
                idx = 66
        if abs(dx) == 1 and dy == -1:
            if underpromote == "rook":
                idx = 67
            if underpromote == "knight":
                idx = 68
            if underpromote == "bishop":
                idx = 69
        if abs(dx) == 1 and dy == 1:
            if underpromote == "rook":
                idx = 70
            if underpromote == "knight":
                idx = 71
            if underpromote == "bishop":
                idx = 72
    encoded[i,j,idx] = 1
    encoded = encoded.reshape(-1); encoded = np.where(encoded==1)[0][0] #index of action
    return encoded

def decode_action(board,encoded):
    encoded_a = np.zeros([4672]); encoded_a[encoded] = 1; encoded_a = encoded_a.reshape(8,8,73)
    a,b,c = np.where(encoded_a == 1); # i,j,k = i[0],j[0],k[0]
    i_pos, f_pos, prom = [], [], []
    for pos in zip(a,b,c):
        i,j,k = pos
        initial_pos = (i,j)
        promoted = None
        if 0 <= k <= 13:
            dy = 0
            if k < 7:
                dx = k - 7
            else:
                dx = k - 6
            final_pos = (i + dx, j + dy)
        elif 14 <= k <= 27:
            dx = 0
            if k < 21:
                dy = k - 21
            else:
                dy = k - 20
            final_pos = (i + dx, j + dy)
        elif 28 <= k <= 41:
            if k < 35:
                dy = k - 35
            else:
                dy = k - 34
            dx = dy
            final_pos = (i + dx, j + dy)
        elif 42 <= k <= 55:
            if k < 49:
                dx = k - 49
            else:
                dx = k - 48
            dy = -dx
            final_pos = (i + dx, j + dy)
        elif 56 <= k <= 63:
            if k == 56:
                final_pos = (i+2,j-1)
            elif k == 57:
                final_pos = (i+2,j+1)
            elif k == 58:
                final_pos = (i+1,j-2)
            elif k == 59:
                final_pos = (i-1,j-2)
            elif k == 60:
                final_pos = (i-2,j+1)
            elif k == 61:
                final_pos = (i-2,j-1)
            elif k == 62:
                final_pos = (i-1,j+2)
            elif k == 63:
                final_pos = (i+1,j+2)
        else:
            if k == 64:
                if board.player == 0:
                    final_pos = (i-1,j)
                    promoted = "R"
                if board.player == 1:
                    final_pos = (i+1,j)
                    promoted = "r"
            if k == 65:
                if board.player == 0:
                    final_pos = (i-1,j)
                    promoted = "N"
                if board.player == 1:
                    final_pos = (i+1,j)
                    promoted = "n"
            if k == 66:
                if board.player == 0:
                    final_pos = (i-1,j)
                    promoted = "B"
                if board.player == 1:
                    final_pos = (i+1,j)
                    promoted = "b"
            if k == 67:
                if board.player == 0:
                    final_pos = (i-1,j-1)
                    promoted = "R"
                if board.player == 1:
                    final_pos = (i+1,j-1)
                    promoted = "r"
            if k == 68:
                if board.player == 0:
                    final_pos = (i-1,j-1)
                    promoted = "N"
                if board.player == 1:
                    final_pos = (i+1,j-1)
                    promoted = "n"
            if k == 69:
                if board.player == 0:
                    final_pos = (i-1,j-1)
                    promoted = "B"
                if board.player == 1:
                    final_pos = (i+1,j-1)
                    promoted = "b"
            if k == 70:
                if board.player == 0:
                    final_pos = (i-1,j+1)
                    promoted = "R"
                if board.player == 1:
                    final_pos = (i+1,j+1)
                    promoted = "r"
            if k == 71:
                if board.player == 0:
                    final_pos = (i-1,j+1)
                    promoted = "N"
                if board.player == 1:
                    final_pos = (i+1,j+1)
                    promoted = "n"
            if k == 72:
                if board.player == 0:
                    final_pos = (i-1,j+1)
                    promoted = "B"
                if board.player == 1:
                    final_pos = (i+1,j+1)
                    promoted = "b"
        if board.current_board[i,j] in ["P","p"] and final_pos[0] in [0,7] and promoted == None: # auto-queen promotion for pawn
            if board.player == 0:
                promoted = "Q"
            else:
                promoted = "q"
        i_pos.append(initial_pos); f_pos.append(final_pos), prom.append(promoted)
    return i_pos, f_pos, prom
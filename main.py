import chess
import numpy as np

pieceVals = {'P': 100, 'N': 300, 'B': 300, 'R': 500, 'Q': 900, 'K': 20000, 'p': -100, 'n': -300, 'b': -300, 'r': -500, 'q': -900, 'k': -20000}


pieceSquareTables = {'P': np.array([[0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
                                    [5.,  10.,  10., -20., -20.,  10.,  10.,   5.],
                                    [5.,  -5., -10.,   0.,   0., -10.,  -5.,   5.],
                                    [0.,   0.,   0.,  20.,  20.,   0.,   0.,   0.],
                                    [5.,   5.,  10.,  25.,  25.,  10.,   5.,   5.],
                                    [10.,  10.,  20.,  30.,  30.,  20.,  10.,  10.],
                                    [50.,  50.,  50.,  50.,  50.,  50.,  50.,  50.],
                                    [0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.]]),
                     'N': np.array([[-50., -40., -30., -30., -30., -30., -40., -50.],
                                    [-40., -20.,   0.,   0.,   0.,   0., -20., -40.],
                                    [-30.,   0.,  10.,  15.,  15.,  10.,   0., -30.],
                                    [-30.,   5.,  15.,  20.,  20.,  15.,   5., -30.],
                                    [-30.,   0.,  15.,  20.,  20.,  15.,   0., -30.],
                                    [-30.,   5.,  10.,  15.,  15.,  10.,   5., -30.],
                                    [-40., -20.,   0.,   5.,   5.,   0., -20., -40.],
                                    [-50., -40., -30., -30., -30., -30., -40., -50.]]),
                     'B': np.array([[-20., -10., -10., -10., -10., -10., -10., -20.],
                                   [-10.,   5.,   0.,   0.,   0.,   0.,   5., -10.],
                                   [-10.,  10.,  10.,  10.,  10.,  10.,  10., -10.],
                                   [-10.,   0.,  10.,  10.,  10.,  10.,   0., -10.],
                                   [-10.,   5.,   5.,  10.,  10.,   5.,   5., -10.],
                                   [-10.,   0.,   5.,  10.,  10.,   5.,   0., -10.],
                                   [-10.,   0.,   0.,   0.,   0.,   0.,   0., -10.],
                                   [-20., -10., -10., -10., -10., -10., -10., -20.]]),
                     'R': np.array([[ 0.,  0.,  0.,  5.,  5.,  0.,  0.,  0.],
                                   [-5.,  0.,  0.,  0.,  0.,  0.,  0., -5.],
                                   [-5.,  0.,  0.,  0.,  0.,  0.,  0., -5.],
                                   [-5.,  0.,  0.,  0.,  0.,  0.,  0., -5.],
                                   [-5.,  0.,  0.,  0.,  0.,  0.,  0., -5.],
                                   [-5.,  0.,  0.,  0.,  0.,  0.,  0., -5.],
                                   [ 5., 10., 10., 10., 10., 10., 10.,  5.],
                                   [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]]),
                     'Q': np.array([[-20., -10., -10.,  -5.,  -5., -10., -10., -20.],
                                   [-10.,   0.,   5.,   0.,   0.,   0.,   0., -10.],
                                   [-10.,   5.,   5.,   5.,   5.,   5.,   0., -10.],
                                   [ -5.,   0.,   5.,   5.,   5.,   5.,   0.,  -5.],
                                   [ -5.,   0.,   5.,   5.,   5.,   5.,   0.,  -5.],
                                   [-10.,   0.,   5.,   5.,   5.,   5.,   0., -10.],
                                   [-10.,   0.,   0.,   0.,   0.,   0.,   0., -10.],
                                   [-20., -10., -10.,  -5.,  -5., -10., -10., -20.]]),
                     'K': np.array([[ 20.,  30.,  10.,   0.,   0.,  10.,  30.,  20.],
                                   [ 20.,  20.,   0.,   0.,   0.,   0.,  20.,  20.],
                                   [-10., -20., -20., -20., -20., -20., -20., -10.],
                                   [-20., -30., -30., -40., -40., -30., -30., -20.],
                                   [-30., -40., -40., -50., -50., -40., -40., -30.],
                                   [-30., -40., -40., -50., -50., -40., -40., -30.],
                                   [-30., -40., -40., -50., -50., -40., -40., -30.],
                                   [-30., -40., -40., -50., -50., -40., -40., -30.]])}

#def evaluationFunction(board):
    evalSum = 0
    pieces = board.piece_map()
    for index in pieces:
        file = chess.square_file(index)
        rank = chess.square_rank(index)
        currentPiece = str(pieces[index])
        table = pieceSquareTables[currentPiece.upper()]
        if currentPiece.isupper():
            flippedTable = np.flip(table, axis=0)
            evalSum += pieceVals[currentPiece] + flippedTable[rank, file]
        else:
            evalSum += pieceVals[currentPiece] - table[rank, file]
    return evalSum

def evaluationFunction(board):
 evalSum = 0
 if board.is_checkmate():
     return -20000 if board.turn else 20000
 for index in range(0, 64):
     piece = str(board.piece_at(index))
     if piece == 'None':
         continue
     table = pieceSquareTables[piece.upper()]
     if piece.isupper():
         evalSum += pieceVals[piece] + table[chess.square_rank(index), chess.square_file(index)]
     else:
         flippedTable = np.flip(table, axis=0)
         evalSum += pieceVals[piece] - flippedTable[chess.square_rank(index), chess.square_file(index)]
 return evalSum

def evaluateMove(board, move):
 if move.promotion:
     return 1000 if board.turn else -1000
 piece = board.piece_at(move.from_square)
 positionalValue = evaluatePosition(piece, move.to_square) - evaluatePosition(piece, move.from_square)
 captureValue = 0
 if board.is_capture(move):
     if board.is_en_passant(move):
         captureValue = 100 if board.turn else -100
     else:
         otherPiece = board.piece_at(move.to_square)
         captureValue = -1*pieceVals[str(otherPiece)]
 return positionalValue + captureValue

def evaluatePosition(piece, square):
 table = pieceSquareTables[str(piece).upper()]
 if str(piece).isupper():
     return table[chess.square_rank(square), chess.square_file(square)]
 else:
     flippedTable = np.flip(table, axis=0)
     return -flippedTable[chess.square_rank(square), chess.square_file(square)]

def orderMoves(board):
 def key(move):
     return evaluateMove(board, move)
 return sorted(board.legal_moves, key = key, reverse = board.turn == True)

def minimax(board, depth, maximizingPlayer, alpha = -1*float('inf'), beta = float('inf')):
  bestMove = None
  if depth == 0 or board.is_game_over():
    return 0, evaluationFunction(board)
  if maximizingPlayer:
    maxEval = -1*float('inf')
    for move in orderMoves(board):
      board.push(move)
      newEval = minimax(board, depth -1, False, alpha, beta)[1]
      board.pop()
      if newEval > maxEval:
        maxEval = newEval
        bestMove = move
      alpha = max(alpha, newEval)
      if alpha >= beta:
        break
    return bestMove, maxEval
  if not maximizingPlayer:
    minEval = float('inf')
    for move in ordderMoves(board):
      board.push(move)
      newEval= minimax(board, depth -1, True, alpha, beta)[1]
      board.pop()
      if newEval < minEval:
          minEval = newEval
          bestMove = move
      beta = min(beta, newEval)
      if alpha >= beta:
        break
    return bestMove, minEval

def playChess(board, maximizingPlayer):
    state = board.is_game_over()
    if state:
        print("Game Over. ", "Black " if board.turn else "White ", "wins")
    else:
        if board.turn == maximizingPlayer:
            print("Playing move...\n")
            board.push(minimax(board, 6, maximizingPlayer)[0])
            print(board)
        else:
            try:
                board.push_san((input("Enter your move, e.g e4:\n")))
                print(board)
            except (ValueError, NameError):
                print("Invalid move, please try again.\n")
        playChess(board, maximizingPlayer)

if __name__ == '__main__':
    chessboard = chess.Board()
    playChess(chessboard, False)

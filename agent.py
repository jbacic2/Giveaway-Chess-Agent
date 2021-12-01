from typing import Set, Tuple
import chess
from board import ChessBoard

MAX_DEPTH = 10
WIN_SCORE = 100000
LOSS_SCORE = -1*WIN_SCORE
DRAW_SCORE = 0

class GiveawayChessAgent:
    # will keep track of the score in terms of how good it is for the player who's turn it is at root (depth 0)
    def alphaBetaPrune(self, board, depth, isMax, alpha, beta) -> Tuple[float, chess.Move]:
        action = None
        (isEndGame, _) = board.checkIfEndGame()
        if isEndGame or depth == MAX_DEPTH:
            value = self.heuristic(board, depth)
            return (value, action)

        if isMax:
            value = float('-inf')
        else:
            value = float('inf')
        
        legalMoves = board.getLegalMoves()

        for move in legalMoves:
            boardWithMove = board.makeBoardCopy()
            boardWithMove.makeMove(move)

            (moveValue, _) = self.alphaBetaPrune(boardWithMove, depth+1, not isMax, alpha, beta)

            if isMax:
                if moveValue > value:
                    value = moveValue
                    action = move

                if moveValue >= beta:
                    return (value, action)
                
                alpha = max(alpha, value)

            else:
                if moveValue < value:
                    value = moveValue
                    action = move
                
                if moveValue <= alpha:
                    return (value, action)
                
                beta = min(beta, value)
        
        return (value, action)
                 

    def __init__(self, colour = chess.BLACK) -> None:
        self.colour = colour
        self.heuristic = self.pieceValueHeuristic

    
    def pickNextMove(self, board) -> chess.Move:
        (_, move) = self.alphaBetaPrune(board, 0, True, float('inf'), float('-inf'))
        return move
    
    # in this heuristic each piece that belongs to the agent is given a value based on the potential 
    # for that piece to take attack other pieces if a state is an endgame state where the agent wins
    # then the score is WIN_SCORE - depth in the case that it is a state where the agent draws it is 
    # DRAW_SCORE and in the case where the agent loses the state have value LOSS_SCORE + depth 
    def pieceValueHeuristic(self,board, depth) -> int:
        pieceValues = {
            chess.PAWN: 2,
            chess.KING: 1,
            chess.ROOK: 5,
            chess.KNIGHT: 2,
            chess.BISHOP: 6,
            chess.QUEEN: 10
        }

        (isEndGame, score) = board.checkIfEndGame()

        if isEndGame:
            if score == 0:
                return DRAW_SCORE

            elif (score == -1 and board.turn == self.colour) or (score == 1 and board.turn != self.colour):
                # the last move was made by the opponent and they lost or in the last move the agent and they won
                return WIN_SCORE - depth
            
            else:
                return LOSS_SCORE + depth 
        
        # for each piece that belongs the the agent it negatively contributes to the score
        # for each piece that belongs to the opponent it positively contributes to the score
        value = 0
        for square in chess.SQUARES:
            pieceType = board.pieceTypeAt(square)
            if pieceType != None:
                pieceValue = pieceValues[pieceType]
                if board.colourAt(square) == self.colour:
                    value -= pieceValue
                else:
                    value += pieceValue
                        
        return value




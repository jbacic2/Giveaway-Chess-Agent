import chess
import random

class NaiveAgent:

    def __init__(self,colour = chess.BLACK) -> None:
        self.colour = colour

    
    def pickNextMove(self, board) -> chess.Move:
        move = random.choice(tuple(board.getLegalMoves()))
        return move
    
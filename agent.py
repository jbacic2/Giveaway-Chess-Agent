from re import S
from typing import Set, Tuple
import chess
from board import ChessBoard
from enum import Enum
import random

MAX_DEPTH = 3
WIN_SCORE = 1000000
LOSS_SCORE = -1*WIN_SCORE
DRAW_SCORE = 0

class HeuristicType(Enum):
    PIECE_VALUE = 1
    PIECE_VALUE_LOCATION_WEIGHT = 2
    NUMBER_SQUARES_ATTACKED = 3
    AVG = 4
    


class GiveawayChessAgent:

    def __init__(self, heuristicType, colour = chess.BLACK) -> None:
        self.colour = colour
        if heuristicType == HeuristicType.PIECE_VALUE:
            self.heuristic = self.pieceValueHeuristic
        elif heuristicType == HeuristicType.PIECE_VALUE_LOCATION_WEIGHT:
            self.heuristic = self.pieceValueLocationWeightHeuristic
        elif heuristicType == HeuristicType.NUMBER_SQUARES_ATTACKED:
            self.heuristic = self.numberSquaresAttackedHeuristic
        else:
            self.heuristic = self.avgHeuristic

    
    def pickNextMove(self, board) -> chess.Move:
        (_, move) = self.alphaBetaPrune(board, 0, True, float('-inf'),float('inf'))
        return move
    
        # will keep track of the score in terms of how good it is for the player who's turn it is at root (depth 0)
    def alphaBetaPrune(self, board, depth, isMax, alpha, beta) -> Tuple[float, chess.Move]:
        cl = 'WHITE: '
        if self.colour == chess.BLACK:
            cl = 'BLACK: '
        action = None
        (isEndGame, _) = board.checkIfEndGame()
        if isEndGame or depth == MAX_DEPTH:
            value = self.heuristic(board, depth)
            # print('------------------------------------------------------------')
            # board.draw()
            # print(f'{cl}NODE AT DEPTH {depth}, value {value} isEnd or Max Depth')
            return (value, action)

        if isMax:
            value = float('-inf')
        else:
            value = float('inf')
        
        legalMoves = list(board.getLegalMoves())
        random.shuffle(legalMoves)

        for move in legalMoves:
            boardWithMove = board.makeBoardCopy()
            boardWithMove.makeMove(move)

            (moveValue, _) = self.alphaBetaPrune(boardWithMove, depth+1, not isMax, alpha, beta)

            if isMax:
                if moveValue > value:
                    value = moveValue
                    action = move

                if moveValue >= beta:
                    # print('------------------------------------------------------------')
                    # board.draw()
                    # print(f'{cl}NODE AT DEPTH {depth}, value {value} move value is greater than beta of {beta}')
                    return (value, action)
                
                alpha = max(alpha, value)

            else:
                if moveValue < value:
                    value = moveValue
                    action = move
                
                if moveValue <= alpha:
                    # print('------------------------------------------------------------')
                    # board.draw()
                    # print(f'{cl}NODE AT DEPTH {depth}, value {value} move value is less than alpha of {alpha}')
                    return (value, action)
                
                beta = min(beta, value)
        # print('------------------------------------------------------------')
        # board.draw()
        # print(f'{cl}NODE AT DEPTH {depth}, value {value} All moves have been checked')
        return (value, action)
                 
    
    # in this heuristic each piece that belongs to the agent is given a value based on the potential 
    # for that piece to take attack other pieces. If a state is an endgame state where the agent wins
    # then the score is WIN_SCORE - depth in the case that it is a state where the agent draws it is 
    # DRAW_SCORE and in the case where the agent loses the state have value LOSS_SCORE + depth 
    def pieceValueHeuristic(self, board, depth) -> int:
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
                # board.draw()
                # color = 'white'
                # if self.colour == chess.BLACK:
                #     color = 'black'
                # print("MYSELF AS {color} WINS")

                return WIN_SCORE - depth
            
            else:
                # board.draw()
                # color = 'white'
                # if self.colour == chess.BLACK:
                #     color = 'black'
                # print("MYSELF AS {color} LOST")
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

    # square is central if in the region of the board [c,f] and [3,6]
    # returns 2 if in inner most 2 by 2 square, 1.5 if in the ring of width 2 around the center and 1 otherwise 
    def squareCentralnessFactor(self, square) -> int:
        centralSquares = {
            chess.D4, chess.D5,  
            chess.E4, chess.E5, 
        } 
        if square in centralSquares:
            return 1.7
        semiCentralSquares = {
            chess.C3, chess.C4, chess.C5, chess.C6, 
            chess.D3, chess.D6, 
            chess.E3, chess.E6, 
            chess.E3, chess.E4, chess.E5, chess.E6
        } 
        if square in semiCentralSquares:
            return 1.3
        return 1
    
    # square is in colour's end if it is in the two rows where colours pieces start at the begining of the game 
    def isInOpponentEnd(self, square, ownColour) -> bool:
        if ownColour == chess.WHITE:
            #then Opponent is black
            endSquares = {
                chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8,
                chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7
            }
        else:
            endSquares = {
                chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1,
                chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2
            }
        return square in endSquares


 # in this heuristic each piece that belongs to the agent is given a value based on the potential 
    # for that piece to take attack other pieces. If a state is an endgame state where the agent wins
    # then the score is WIN_SCORE - depth in the case that it is a state where the agent draws it is 
    # DRAW_SCORE and in the case where the agent loses the state have value LOSS_SCORE + depth 
    def pieceValueLocationWeightHeuristic(self,board, depth) -> float:
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
        opponentPieceValue = 0
        ownPieceValue = 0
        opponentNumberPieces = 0
        ownNumberPieces = 0
        for square in chess.SQUARES:
            pieceType = board.pieceTypeAt(square)
            if pieceType != None:

                pieceValue = pieceValues[pieceType]*self.squareCentralnessFactor(square)

                if self.isInOpponentEnd(square, board.colourAt(square)):
                    pieceValue = pieceValue*1.1

                if board.colourAt(square) == self.colour:
                    
                    ownPieceValue += pieceValue
                    ownNumberPieces += 1
                else:
                    opponentPieceValue += pieceValue
                    opponentNumberPieces+= 1 
                        
        return opponentPieceValue - ownPieceValue

    # in this heuristic favours minimizing the ratio of squares that the bot is attacking and 
    # maximizing the number of squares the opponent is attacking If a state is an endgame state where the agent wins
    # then the score is WIN_SCORE - depth in the case that it is a state where the agent draws it is 
    # DRAW_SCORE and in the case where the agent loses the state have value LOSS_SCORE + depth 
    def numberSquaresAttackedHeuristic(self, board, depth) -> int:

        (isEndGame, score) = board.checkIfEndGame()

        if isEndGame:
            if score == 0:
                return DRAW_SCORE

            elif (score == -1 and board.turn == self.colour) or (score == 1 and board.turn != self.colour):
                # the last move was made by the opponent and they lost or in the last move the agent and they won
                return WIN_SCORE - depth
            
            else:
                return LOSS_SCORE + depth 
        
        value = -1* len(board.squaresAttackedByColour(self.colour))

        opponentColour = chess.WHITE 
        if self.colour == chess.WHITE:
            opponentColour = chess.BLACK
        
        value += len(board.squaresAttackedByColour(opponentColour))
                        
        return value
    
    # in this heuristic favours minimizing the ratio of squares that the bot is attacking and 
    # maximizing the number of squares the opponent is attacking If a state is an endgame state where the agent wins
    # then the score is WIN_SCORE - depth in the case that it is a state where the agent draws it is 
    # DRAW_SCORE and in the case where the agent loses the state have value LOSS_SCORE + depth 
    def avgHeuristic(self, board, depth) -> int:

        pieceValueHeuristic = self.pieceValueHeuristic(board, depth)
        numberSquaresAttackedHeuristic = self.pieceValueHeuristic(board,depth)

        return (pieceValueHeuristic + numberSquaresAttackedHeuristic) /2



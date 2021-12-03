from typing import Tuple
from board import ChessBoard
from agent import GiveawayChessAgent, HeuristicType
import textColour

class ChessGame:
    def __init__(self):
        self.gameBoard = ChessBoard()
        self.agent = GiveawayChessAgent(HeuristicType.PIECE_VALUE_LOCATION_WEIGHT)
        self.gameBoard.draw()

    def agentMove(self):
        print(f'{textColour.PINK}=================================================={textColour.END}')
        move = self.agent.pickNextMove(self.gameBoard)
        print(f'Agent Moves {move}')
        (isEndGame, score) = self.gameBoard.makeMove(move)

        self.gameBoard.draw()

        if isEndGame:
            if score == 1:
                print(f'{textColour.CYAN}Looks like the agent won, Better luck next time!{textColour.END}')
            elif score == -1:
                print(f'{textColour.CYAN}Congrats you beat the agent{textColour.END}')
            else: 
                print(f'{textColour.CYAN}Ended in a draw!!{textColour.END}')
        
        return isEndGame
    
    def __getFromSquare(self) -> str:
        fromSquareStr = input("Enter the current square of the piece you want to move: ")
        (isValid, msg) = self.gameBoard.validateFromSquare(fromSquareStr)
        while not isValid:
            print(f'{textColour.PINK}=================================================={textColour.END}')
            print(msg)
            print('Please enter a new start square.')
            fromSquareStr = input("Enter the current square of the piece you want to move: ")
            (isValid, msg) = self.gameBoard.validateFromSquare(fromSquareStr)
        
        return (fromSquareStr, msg)

    # returns isEndGame boolean
    def playerMove(self) -> bool:
        promotedPieceStr = None

        print(f'{textColour.PINK}=================================================={textColour.END}')
        (fromSquareStr, fromSquareMsg) = self.__getFromSquare()
        toSquareStr = input(fromSquareMsg)

        (isValid, needsPawnPromotion, msg) = self.gameBoard.validateMove(fromSquareStr, toSquareStr)
        while needsPawnPromotion:
            print(msg)
            promotedPieceStr = input("Enter N, B, R, Q or K: ")
            (isValid, needsPawnPromotion, msg) = self.gameBoard.validateMove(fromSquareStr, toSquareStr,promotedPieceStr)

        while not isValid:
            print(f'{textColour.PINK}=================================================={textColour.END}')
            print(msg)
            print('Please enter a new move.')
            (fromSquareStr, fromSquareMsg) = self.__getFromSquare()
            toSquareStr = input(fromSquareMsg)
            (isValid, needsPawnPromotion, msg) = self.gameBoard.validateMove(fromSquareStr, toSquareStr)

            while needsPawnPromotion:
                print(msg)
                promotedPieceStr = input("Enter N, B, R, Q or K: ")
                (isValid, needsPawnPromotion, msg) = self.gameBoard.validateMove(fromSquareStr, toSquareStr,promotedPieceStr)

        
        (isEndGame, score) = self.gameBoard.makeMoveFromInput(fromSquareStr,toSquareStr,promotedPieceStr)

        self.gameBoard.draw()

        if isEndGame:
            if score == 1:
                print(f'{textColour.CYAN}Congrats!!! You won!!{textColour.END}')
            elif score == -1:
                print(f'{textColour.CYAN}Sorry, you lost{textColour.END}')
            else: 
                print(f'{textColour.CYAN}Ended in a draw!!{textColour.END}')
        
        return isEndGame
    
    def playGame(self):
        while True:
            isEndGame =  self.playerMove()
            if isEndGame:
                break
            isEndGame = self.agentMove()
            if isEndGame:
                break

game = ChessGame()
game.playGame()


    

    

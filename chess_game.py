from board import ChessBoard
from agent import GiveawayChessAgent

class ChessGame:
    def __init__(self):
        self.gameBoard = ChessBoard()
        self.agent = GiveawayChessAgent()
        self.gameBoard.draw()

    def agentMove(self):
        move = self.agent.pickNextMove(self.gameBoard)
        #self.gameBoard.makeMove(move)
        self.gameBoard.draw()
    
    def playerMove(self):
        move = input("What's your next move? ")
        isValid = self.gameBoard.makeMove(move)
        while not isValid:
            print('Sorry, that was not a valid move.')
            move = input("Please enter a new move: ")
        isValid = self.gameBoard.makeMove(move)
        self.gameBoard.draw()
    
    def playGame(self):
        self.__init__()
        while True:
            self.playerMove()
            self.playerMove()
            #self.agentMove()



    

    

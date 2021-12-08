from typing import Tuple

import chess
from board import ChessBoard
from agent import GiveawayChessAgent, HeuristicType
from naiveAgent import NaiveAgent

TRIALS = 10

# return 1 if player1 wins, -1 if player2 and 0 if its a draw
def playGame(player1, player2):

    gameBoard = ChessBoard()
    numMove = 0

    while True:
        move = player1.pickNextMove(gameBoard)
        (isEndGame, score) = gameBoard.makeMove(move)
        if isEndGame:
            return score
        move = player2.pickNextMove(gameBoard)
        (isEndGame, score) = gameBoard.makeMove(move)
        if isEndGame:
            return score*-1
        numMove += 1
        print(f'have made {numMove} moves')
        if numMove % 10 == 0:
            gameBoard.draw()

def runTests(player1, player2):
    player1Wins = 0
    player2Wins = 0

    for i in range(TRIALS):
        result = playGame(player1, player2)
        if result == 1:
            player1Wins += 1
        elif result == -1:
            player2Wins += 1
    
    return (player1Wins, player2Wins)

def chessBotVersusNaive(heuristicType):
    naive = NaiveAgent()
    chessBot = GiveawayChessAgent(heuristicType, chess.BLACK)

    (naiveWinsWhite, chessBotWinsBlack) = runTests(naive, chessBot)

    chessBot = GiveawayChessAgent(heuristicType, chess.WHITE)

    (chessBotWinsWhite, naiveWinsBlack) = runTests(chessBot, naive)

    print('   Number wins   |         heuristic wins      |      naive bot wins')
    print('---------------------------------------------------------------------------------')
    print(f'  BLACK           |          {chessBotWinsBlack}              |             {naiveWinsBlack}')
    print('---------------------------------------------------------------------------------')
    print(f'  WHITE           |          {chessBotWinsWhite}              |             {naiveWinsWhite}')

def heuristicVersusHeuristic(heuristicType1, heuristicType2):
    type1Agent = GiveawayChessAgent(heuristicType1, chess.BLACK)
    type2Agent = GiveawayChessAgent(heuristicType2, chess.WHITE)

    (type2WinsWhite, type1WinsBlack) = runTests(type2Agent, type1Agent)

    type1Agent = GiveawayChessAgent(heuristicType1, chess.WHITE)
    type2Agent = GiveawayChessAgent(heuristicType2, chess.BLACK)

    (type1WinsWhite, type2WinsBlack) = runTests(type1Agent,type2Agent)

    print('   Number wins     |         heuristic  1 wins    |      heuristic  2 wins ')
    print('---------------------------------------------------------------------------------')
    print(f'  BLACK           |          {type1WinsBlack}              |             {type2WinsBlack}')
    print('---------------------------------------------------------------------------------')
    print(f'  WHITE           |          {type1WinsWhite}              |             {type2WinsWhite}')

# print('Piece Value Heuristic vs Naive')
# chessBotVersusNaive(HeuristicType.PIECE_VALUE)
# print()

# print('Piece Value Location Weight Heuristic vs Naive')
# chessBotVersusNaive(HeuristicType.PIECE_VALUE_LOCATION_WEIGHT)
# print()

# print('Number Squares Attacked Heuristic vs Naive')
# chessBotVersusNaive(HeuristicType.NUMBER_SQUARES_ATTACKED)
# print()

print('Piece Value Heuristic (type 1) vs Piece Value Location Weight Heuristic (type 2)')
heuristicVersusHeuristic(HeuristicType.PIECE_VALUE, HeuristicType.PIECE_VALUE_LOCATION_WEIGHT)
print()

# print('Piece Value Heuristic (type 1) vs Number Squares Attacked (type 2)')
# heuristicVersusHeuristic(HeuristicType.PIECE_VALUE, HeuristicType.NUMBER_SQUARES_ATTACKED)
# print()

# print('Number Squares Attacked (type 1) vs Piece Value Location Weight Heuristic (type 2)')
# heuristicVersusHeuristic(HeuristicType.NUMBER_SQUARES_ATTACKED, HeuristicType.PIECE_VALUE_LOCATION_WEIGHT)
# print()
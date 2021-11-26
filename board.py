import chess
import chess.variant

class ChessBoard:
    def __init__(self) -> None:
        self.__board = chess.Board()

    def draw(self) -> None:
        yellow = '\033[93m'
        blue = '\033[94m'
        red = '\033[91m'
        endColour = '\033[0m'

        print(f'{yellow}  a b c d e f g h')
        print(f'  ---------------{endColour}')
        for row in range(7,-1,-1):
             for col in range(-1,8):
                if col == -1:
                    print(f'{yellow}{str(row+1)}|{endColour}', end = "")
                else:
                    square = row*8+col
                    piece = self.__board.piece_at(square)
                    if (piece == None):
                        if (row+col) % 2 == 0:
                            print(" ", end = " ")
                        else:
                            print(f'{blue}X{endColour}', end = " ")
                    else:
                        if self.__board.color_at(square) == chess.BLACK:
                            print(f'{red}{piece}{endColour}', end = " ")
                        else:
                            print(piece, end=" ")
             print("")
    
    def makeMove(move:str) -> bool:
        

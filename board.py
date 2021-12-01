from typing import Set, Tuple
import chess
import chess.variant
import textColour

class ChessBoard:
    def __init__(self, fenStr = None) -> None:
        if fenStr == None:
            self.board = chess.variant.GiveawayBoard()
        else:
            self.board = chess.variant.GiveawayBoard(fenStr)
        #self.board = chess.variant.GiveawayBoard('b7/PPPP4/8/8/8/4pppp/8/8')
        #self.board = chess.Board('b7/PPPP4/8/8/8/4pppp/8/8')

    def pieceTypeAt(self, square) -> chess.PieceType:
        return self.board.piece_type_at(square)
        
    def colourAt(self, square):
        return self.board.color_at(square)
    
    def turn(self):
        return self.board.turn

    def draw(self) -> None:
        print(f'{textColour.YELLOW}  a b c d e f g h')
        print(f'  ---------------{textColour.END}')

        for row in range(7,-1,-1):
             for col in range(-1,9):
                if col == -1:
                    print(f'{textColour.YELLOW}{str(row+1)}|{textColour.END}', end = "")
                elif col == 8:
                    print(f'{textColour.YELLOW}|{str(row+1)}{textColour.END}', end = "")
                else:
                    square = row*8+col
                    piece = self.board.piece_at(square)
                    if (piece == None):
                        if (row+col) % 2 == 0:
                            print(" ", end = " ")
                        else:
                            print(f'{textColour.BLUE}{chr(219)}{textColour.END}', end = " ")
                    else:
                        if self.board.color_at(square) == chess.BLACK:
                            print(f'{textColour.RED}{piece}{textColour.END}', end = " ")
                        else:
                            print(piece, end=" ")
             print("")

        print(f'{textColour.YELLOW}  ---------------')
        print(f'  a b c d e f g h{textColour.END}')

    # retruns a list of all chess moves in which the player of <colour> can capture the opponents piece
    def allCaptureMoves(self,colour) -> Set[chess.Move]:
        pseudoLegalMoves = self.board.pseudo_legal_moves
        captureMoves = set()
        # loop through each square
        for square in chess.SQUARES:
            if self.board.color_at(square) == colour:
                for attackedSquare in self.board.attacks(square):
                    if self.board.piece_at(attackedSquare):
                        move = chess.Move(square,attackedSquare)
                        if move in pseudoLegalMoves:
                            captureMoves.add(move)
                        # when checking if a move where the pawn is promoted is valid will always check with a rook
                        moveWithRookPromotion = chess.Move(square,attackedSquare,chess.ROOK)
                        if moveWithRookPromotion in pseudoLegalMoves:
                            captureMoves.add(moveWithRookPromotion)
        
        return captureMoves

    def getLegalMoves(self) -> Set[chess.Move]:
        allCaptureMoves = self.allCaptureMoves(self.board.turn)
        if len(allCaptureMoves) > 0:
            return allCaptureMoves
        
        legalMoves = set()
        for move in self.board.pseudo_legal_moves:
            if not self.board.is_castling(move):
                legalMoves.add(move)
        
        return legalMoves

    def makeBoardCopy(self):
        return ChessBoard(self.board.fen())

    # checks the the current square contains a piece of the current player 
    def validateFromSquare(self, fromSquareStr:str) -> Tuple[bool,str]:

        try:
            fromSquareStr.strip()
            fromSquare = chess.parse_square(fromSquareStr)
        except:
            msg = f'{textColour.YELLOW}You entered an invalid square. Enter square as <letter><number>.{textColour.END}'
            return (False, msg)
        
        if self.board.piece_at(fromSquare) == None:
            msg = f'{textColour.YELLOW}The start square you chose does not contain a piece.{textColour.END}'
            return(False, msg)

        if self.board.color_at(fromSquare) != self.board.turn:
            msg = f'{textColour.YELLOW}The start square you chose does not contain a piece of your colour.{textColour.END}'
            return(False, msg)
        
        if self.board.turn == chess.BLACK:
            msg = f'Moving piece {textColour.RED}{self.board.piece_at(fromSquare)}{textColour.END} to square: '
        else:
            msg = f'Moving piece {self.board.piece_at(fromSquare)} to square: '
        return (True,msg)


    #checks if it board is at end game returns (isEndGame, score)
    # score is 1 if the last move made resulted in that player winning, -1 if the last player to move lost, 0 otherwise
    def checkIfEndGame(self) -> Tuple[bool, int]:

        isEndGame = False

        endScore = 0 

        if self.board.is_variant_win():
            # last player to move lost
            endScore = -1
            isEndGame = True

        elif self.board.is_variant_loss():
            # last player to move wins
            endScore = 1
            isEndGame = True
        
        elif self.board.is_variant_draw():
            endScore = 0
            isEndGame = True
        
        return (isEndGame, endScore)
    
    # check if a move is valid or if it needs a piece type for promotion 
    # returns (isValid, needsPawnPromotion, errorMessage)
    def validateMove(self, fromSquareStr:str, toSquareStr:str, promotedPieceStr: str = None) -> Tuple[bool,bool,str]:
        (isFromValid, msg) = self.validateFromSquare(fromSquareStr)
        if not isFromValid:
            return (False, False, msg)

        fromSquareStr.strip()
        fromSquare = chess.parse_square(fromSquareStr)

        # validating to square
        try:
            toSquareStr.strip()
            toSquare = chess.parse_square(toSquareStr)
        except:
            msg = f'{textColour.YELLOW}You entered an invalid square. Enter square as <letter><number>{textColour.END}'
            return (False, False, msg)
        
        isPawnPromotion = False 
        if (self.board.piece_type_at(fromSquare) == chess.PAWN) and toSquare in {chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1, chess.A8, chess.B8, chess.C8, chess.D8, chess.E8,chess.F8, chess.G8, chess.H8}:
            isPawnPromotion = True
        
        if isPawnPromotion:
            # use rook as defult promoted piece while validating promotion 
            move = chess.Move(fromSquare, toSquare, chess.ROOK)
        else:
            move = chess.Move(fromSquare, toSquare)


        if self.board.is_castling(move):
            msg = f'{textColour.YELLOW}You can not castle in Give Away Chess.{textColour.END}'
            return (False, False, msg)

        if not move in self.board.pseudo_legal_moves:
            msg = f'{textColour.YELLOW}This is not a legal move.{textColour.END}'
            return (False, False, msg)
        
        # ensuring that the player has captured a piece if they can 
        allCaptureMoves = self.allCaptureMoves(self.board.turn)
        
        if len(allCaptureMoves) > 0 and move not in allCaptureMoves:
            msg = f'{textColour.YELLOW}It is possible for you to capture a piece. \nIn Giveaway Chess, if you can capture a piece you must take it.{textColour.END}'
            return (False, False, msg)
        
        if isPawnPromotion and promotedPieceStr == None:
            msg = 'Your pawn has reached the end of the board. What piece would you like to promote it to?'
            return (False, True, msg)
        
        if isPawnPromotion:
            try:
                promotedPieceStr.strip()
                if self.board.turn == chess.BLACK:
                    promotedPieceStr = promotedPieceStr.lower()
                else:
                    promotedPieceStr = promotedPieceStr.upper()
                promotedPiece = chess.Piece.from_symbol(promotedPieceStr)
            except:
                msg = f'{textColour.YELLOW}This is not a valid chess piece.{textColour.END}'
                return(False, True, msg)
        
            if promotedPiece == chess.PAWN:
                msg = f'{textColour.YELLOW}You cannot promote a pawn to a pawn.{textColour.END}'
                return(False, True, msg)
            
        return(True, False, 'SUCCESS')

    # moves piece at fromSquareStr toSquareStr and if it is a pawn promotion, pawn is promoted to promotedPieceStr
    # throws an error if invalid input 
    # returns (isEndGame, score)
    def makeMoveFromInput(self, fromSquareStr:str, toSquareStr:str, promotedPieceStr: str = None) -> Tuple[bool, int]:
        fromSquareStr.strip()
        fromSquare = chess.parse_square(fromSquareStr)

        toSquareStr.strip()
        toSquare = chess.parse_square(toSquareStr)

        if promotedPieceStr:
            promotedPieceStr.strip()
        
            if self.board.turn == chess.BLACK:
                promotedPieceStr = promotedPieceStr.lower()
            else:
                promotedPieceStr = promotedPieceStr.upper()

            promotedPiece = chess.Piece.from_symbol(promotedPieceStr)
            
            move = chess.Move(fromSquare, toSquare, promotedPiece)
            self.board.push(move) 

            # update promoted piece
            self.board.set_piece_at(toSquare, promotedPiece, True)

        else:
            move = chess.Move(fromSquare, toSquare)
            self.board.push(move)
        
        return self.checkIfEndGame()

    # moves piece at fromSquareStr toSquareStr and if it is a pawn promotion, pawn is promoted to promotedPieceStr
    # throws an error if invalid input 
    # returns (isEndGame, score) score is 1 if the last player to move won, -1 if the last player to moved lost, 0 otherwise
    def makeMove(self, move) -> Tuple[bool, int]:
        
        self.board.push(move) 

        #check of end game
        return self.checkIfEndGame()


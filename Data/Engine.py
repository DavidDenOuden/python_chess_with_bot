"""
responsable for handling the gamestate
"""

import numpy as np

class GameState():
    def __init__(self):
        # board is 8 by 8 whites perspective
        # first character represents color, second represents piece
        # -- means nothing

        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ])
        """
        self.board = np.array([
            ["--", "--", "--", "bN", "bK", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bQ", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "wP", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "wB", "wK", "--", "wN", "wR"],
        ])
        """


        self.board2 = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "--", "--", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ])
        self.white_to_move = True
        self.moves_log = []
        self.gs_log = []
        self.wK_pos = (7,4)
        self.bK_pos = (1,3)#######################################
        self.wK_incheck = False
        self.bK_incheck = False
        self.w_castle_short = True
        self.w_castle_long = True
        self.b_castle_short = True
        self.b_castle_long = True
        self.promotion_next = False
        self.none_captured = 0
        # properties for the bot
        self.all_possible_moves = None
        self.depth = 0
        self.child_gamestates = []
        self.evaluation = None
        self.best_move_index = None


    def makeMove(self, move, en_passant = False, skip = False):
        """main method that makes a move by altering the boardstate and registering the move"""
        if move.pieceMoved[1] == 'P' and en_passant:  # check for en passant
            if move.endCol != move.startCol and move.pieceCaptured == '--':  # this means en passant was moved
                self.board[move.startRow, move.startCol] = "--"
                self.board[move.endRow, move.endCol] = move.pieceMoved
                self.board[move.startRow, move.endCol] = "--"
                move.enpassantmove = True
                self.moves_log.append(move)
                if not skip:  # skip means this part is only done when the move is actually made
                    gamestate = self.boardToString()  # write gamestate to string
                    self.gs_log.append(gamestate)  # save gamestate
                    move.none_captured = self.none_captured  # save the none_captured in the move class
                    self.none_captured = 0  # return to 0 because a pawn was moved
            else:  # follow normal move
                self.board[move.startRow, move.startCol] = "--"
                self.board[move.endRow, move.endCol] = move.pieceMoved
                self.moves_log.append(move)
                if not skip:
                    gamestate = self.boardToString()  # write gamestate to string
                    self.gs_log.append(gamestate)  # save gamestate
                    move.none_captured = self.none_captured  # save the none_captured in the move class
                    self.none_captured = 0  # return to 0 because a pawn was moved

        else: # follow normal move
            self.board[move.startRow, move.startCol] = "--"
            self.board[move.endRow, move.endCol] = move.pieceMoved
            self.moves_log.append(move)
            if not skip:
                gamestate = self.boardToString() # write gamestate to string
                self.gs_log.append(gamestate) # save gamestate
                move.none_captured = self.none_captured  # save the none_captured in the move class
                if move.pieceCaptured == '--':
                    self.none_captured = self.none_captured +1 # add 1 since no pawn was moved or piece was captured
                else:
                    self.none_captured = 0 # reset to 0 since a piece was captured
        if move.pieceMoved[1] == 'K': # update king position so it doesnt have to be found and end all castling rights
            if self.white_to_move:
                move.w_castle_short = self.w_castle_short
                move.w_castle_long = self.w_castle_long
                self.w_castle_short = False
                self.w_castle_long = False
                self.wK_pos = (move.endRow, move.endCol)
            else:
                move.b_castle_short = self.b_castle_short
                move.b_castle_long = self.b_castle_long
                self.b_castle_short = False
                self.b_castle_long = False
                self.bK_pos = (move.endRow, move.endCol)
        elif move.pieceMoved[1] == 'R' and not skip: # end castling rights if rook has moved
            if self.white_to_move:
                if move.startCol == 0:
                    move.w_castle_long = self.w_castle_long
                    self.w_castle_long = False
                elif move.startCol == 7:
                    move.w_castle_short = self.w_castle_short
                    self.w_castle_short = False
            else:
                if move.startCol==0:
                    move.b_castle_long = self.b_castle_long
                    self.b_castle_long = False
                elif move.startCol == 7:
                    move.b_castle_short = self.b_castle_short
                    self.b_castle_short = False
        # additionally move rook if castling
        if move.pieceMoved[1]== 'K' and abs(move.startCol -move.endCol )== 2:
            if move.startRow == 7: #white casltes
                if move.endCol == 6: #short
                    self.board[7][7]='--'
                    self.board[7][5]='wR'
                    move.w_castle_this_move_short = True
                else: #long
                    self.board[7][0]='--'
                    self.board[7][3]='wR'
                    move.w_castle_this_move_long = True
            else:#black castles
                if move.endCol == 6: #short
                    self.board[0][7]='--'
                    self.board[0][5]='bR'
                    move.b_castle_this_move_short = True
                else: #long
                    self.board[0][0]='--'
                    self.board[0][3]='bR'
                    move.b_castle_this_move_long = True
        #if not self.promotion_next: # Only switch turns if there has not been a promotion yet
        self.white_to_move = not self.white_to_move
        #append the king in check information
        """
        color = move.pieceMoved[0]
        if color == 'b':
            bool = self.wK_incheck
        else:
            bool = self.bK_incheck
        move.set_kings_in_check(color, bool)
        """

    def undoMove(self, skip = False):
        """main method that undoes a move by reinstating the boardstate and unregistering it"""
        if len(self.moves_log) > 0:
            move  = self.moves_log[-1]
            self.board[move.endRow,move.endCol] = move.pieceCaptured
            self.board[move.startRow,move.startCol] = move.pieceMoved
            if move.pieceMoved[1]=='K': #update king position so it doesnt have to be found and return all castling rights
                if move.pieceMoved[0]=='w':
                    self.w_castle_short = move.w_castle_short
                    self.w_castle_long = move.w_castle_long
                    self.wK_pos = (move.startRow, move.startCol)
                else:
                    self.b_castle_short = move.b_castle_short
                    self.b_castle_long = move.b_castle_long
                    self.bK_pos = (move.startRow, move.startCol)
            elif move.pieceMoved[1]=='R' and not skip: #return possible castling rights
                if move.pieceMoved[0]=='w':
                    self.w_castle_short = move.w_castle_short
                    self.w_castle_long = move.w_castle_long
                else:
                    self.b_castle_short = move.b_castle_short
                    self.b_castle_long = move.b_castle_long
            elif move.enpassantmove:
                if move.pieceMoved[0] == 'w':
                    self.board[move.startRow, move.endCol] = "bP"
                else:
                    self.board[move.startRow, move.endCol] = "wP"
            if move.w_castle_this_move_short: #return rook when just castled #white short
                self.board[7][7] = 'wR'
                self.board[7][5] = '--'
            elif move.w_castle_this_move_long: #return rook when white just castled long
                self.board[7][0] = 'wR'
                self.board[7][3] = '--'
            elif move.b_castle_this_move_short: #return rook when black just castled short
                self.board[0][7] = 'bR'
                self.board[0][5] = '--'
            elif move.b_castle_this_move_long: #return rook when black just castled long
                self.board[0][0] = 'bR'
                self.board[0][3] = '--'
            del self.moves_log[-1]
            if not skip:
                del self.gs_log[-1]
                self.none_captured = move.none_captured
            #switch player turns
            self.white_to_move = not self.white_to_move
            #retrieve king in check information
            """
            if len(self.moves_log) > 0:
                new_last_move = self.moves_log[-1]
                self.wK_incheck = new_last_move.wk_in_check
                self.bK_incheck = new_last_move.bk_in_check
            """
        else:
            pass

    def boardToString(self):
        """parses the board state to a string, used to check for 3fod repetition"""
        boardstring = ''
        for i in self.board:
            for j in i:
                boardstring = boardstring + j
        return boardstring


    def checkForDrawRepitition(self):
        """method that checks if the game should be drawn by 3fold repitition"""
        if len(self.gs_log) > 0 and self.gs_log.count(self.gs_log[-1])>2:
            print('draw by 3fold repitition')
            return True

    def checkForStalemate(self):
        """method that can check if there is a stalemate situation"""
        if self.white_to_move:
            color = 'w'
            for i, r in enumerate(self.board):
                for j, c in enumerate(r):
                    if c[0] == color:
                        # probably more efficient to start with king right here, but for now this is fine
                        legal_moves = self.getLegalMoves(c, (i, j), False)
                        if len(legal_moves) > 0:
                            return False
                            break
            return True
        else:
            color = 'b'
            for i, r in enumerate(self.board):
                for j, c in enumerate(r):
                    if c[0] == color:
                        # probably more efficient to start with king right here, but for now this is fine
                        legal_moves = self.getLegalMoves(c, (i, j), False)
                        if len(legal_moves) > 0:
                            return False
                            break
            return True

    def checkForCheckmate(self):
        """method to check if the color to move is in checkmate"""
        if self.white_to_move:
            color = 'w'
            self._isKingInCheck(self.wK_pos, color)
            if self.wK_incheck:
                for i, r in enumerate(self.board):
                    for j, c in enumerate(r):
                        if c[0] == color:
                            #probably more efficient to start with king right here, but for now this is fine
                            legal_moves = self.getLegalMoves(c, (i, j), False)
                            if len(legal_moves) >0:
                                return False
                                break
                return True
            else:
                return False
        else:
            color = 'b'
            self._isKingInCheck( self.bK_pos, color)
            if self.bK_incheck:
                for i, r in enumerate(self.board):
                    for j, c in enumerate(r):
                        if c[0] == color:
                            #probably more efficient to start with king right here, but for now this is fine
                            legal_moves = self.getLegalMoves(c, (i, j), False)
                            if len(legal_moves) >0:
                                return False
                                break
                return True

    def _isKingInCheck(self,kingpos,color):
        """method to check if a king is in a check position while evaluating a boardstate"""
        if color == 'w':
            self.wK_incheck = False
            enemy = 'b'
        else:
            self.bK_incheck = False
            enemy = 'w'
        for i, r in enumerate(self.board):
            for j, c in enumerate(r):
                if c[0] == enemy:
                    legal_moves = self.getLegalMoves(c, (i, j), True)
                    if kingpos in legal_moves:
                        if color == 'w':
                            self.wK_incheck = True
                        else:
                            self.bK_incheck = True
                        break
        if color == 'w':
            return self.wK_incheck
        else:
            return self.bK_incheck

    def _isKingInCheckLite(self,kingpos,color):
        """method to check if a king is in a check position while evaluating a boardstate, only considering pieces that can pin, bischops queens and rooks"""
        if color == 'w':
            self.wK_incheck = False
            enemy = 'b'
        else:
            self.bK_incheck = False
            enemy = 'w'
        for i, r in enumerate(self.board):
            for j, c in enumerate(r):
                if c[0] == enemy:
                    if c[1] == 'R' or c[1] == 'B' or c[1] == 'Q':
                        legal_moves = self.getLegalMoves(c, (i, j), True)
                        if kingpos in legal_moves:
                            if color == 'w':
                                self.wK_incheck = True
                            else:
                                self.bK_incheck = True
                            break
        if color == 'w':
            return self.wK_incheck
        else:
            return self.bK_incheck

    def isKingInCheck(self,startSq,endSq,color,en_passant = False):
        """method to check if a king is in a check position while evaluating a boardstate"""
        king_in_check_after_move = False
        move = Move(startSq,endSq,self.board)
        self.makeMove(move, en_passant, True)
        if color == 'w':
            c = self._isKingInCheck(self.wK_pos, color)
            if self.wK_incheck == True:
                king_in_check_after_move = True
        elif color == 'b':
            c = self._isKingInCheck(self.bK_pos,color)
            if self.bK_incheck == True:
                king_in_check_after_move = True
        self.undoMove(True)
        return king_in_check_after_move

    def isKingInCheckLite(self,startSq,endSq,color,en_passant = False):
        """method to check if a king is in a check position while evaluating a boardstate"""
        king_in_check_after_move = False
        move = Move(startSq,endSq,self.board)
        self.makeMove(move, en_passant, True)
        if color == 'w':
            c = self._isKingInCheckLite(self.wK_pos, color)
            if self.wK_incheck == True:
                king_in_check_after_move = True
        elif color == 'b':
            c = self._isKingInCheckLite(self.bK_pos,color)
            if self.bK_incheck == True:
                king_in_check_after_move = True
        self.undoMove(True)
        return king_in_check_after_move

    def getLegalMoves(self,piece,startSq,recursion=False):
        """main method to collect all the legal moves given the type of piece"""
        if piece[1] == 'K':
            legal_moves = self.kingLegalMoves(piece[0],startSq,recursion)
        elif piece[1] == 'P':
            legal_moves = self.pawnLegalMoves(piece[0], startSq,recursion)
        elif piece[1] == 'Q':
            legal_moves = self.queenLegalMoves(piece[0],startSq,recursion)
        elif piece[1] == 'N':
            legal_moves = self.knightLegalMoves(piece[0],startSq,recursion)
        elif piece[1] == 'B':
            legal_moves = self.bishopLegalMoves(piece[0],startSq,recursion)
        elif piece[1] == 'R':
            legal_moves = self.rookLegalMoves(piece[0],startSq,recursion)
        else:
            legal_moves = []
        return legal_moves

    def kingLegalMoves(self,color,position,recursion=False):
        """method to generate the kings legal moves"""
        deltas = [(-1, -1), (-1, 0), (-1, +1), (0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1)]
        possible_positions = [(position[0]+i[0],position[1] + i[1]) for i in deltas]
        legal_moves = []
        for i in possible_positions:
            if i[0] < 0 or i[0] > 7 or i[1] < 0 or i[1] > 7: #positions outside board bounds
                pass
            elif self.board[i[0]][i[1]][0] == color: #trying to take the same color
                pass
            else:
                if not recursion:
                    check = self.isKingInCheck(position, i, color)
                    if recursion == False and check == True:
                        pass
                    else:
                        legal_moves.append(i)
                else:
                    legal_moves.append(i)

        # castling short and long manually
        if recursion == False and color == 'w':
            if self.w_castle_short and self.board[7][5] == '--' and self.board[7][6] == '--': # in between squares are empty and rook nor king hasntmoved
                if self._isKingInCheck((7, 4), 'w') == False and self._isKingInCheck((7, 5), 'w') == False and self._isKingInCheck((7, 6), 'w') == False: #cant castle if any of the squares are guarded!
                    legal_moves.append((7, 6))
            if self.w_castle_long and self.board[7][3] == '--' and self.board[7][2] == '--' and self.board[7][1] == '--': # in between squares are empty and rook nor king hasntmoved
                if self._isKingInCheck((7, 4), 'w') == False and self._isKingInCheck((7, 3), 'w') == False and self._isKingInCheck((7, 2), 'w') == False:  # cant castle if any of the squares are guarded!
                    legal_moves.append((7, 2))
        elif recursion == False and color == 'b':
            if self.b_castle_short and self.board[0][5] == '--' and self.board[0][6] == '--': # in between squares are empty and rook nor king hasntmoved
                if self._isKingInCheck((0, 4), 'b')== False and self._isKingInCheck((0, 5), 'b') == False and self._isKingInCheck((0,6),'b')==False: #cant castle if any of the squares are guarded!
                    legal_moves.append((0, 6))
            if self.b_castle_long and self.board[0][3] == '--' and self.board[0][2]=='--' and self.board[0][1] == '--': # in between squares are empty and rook nor king hasntmoved
                if self._isKingInCheck((0, 4), 'b') == False and self._isKingInCheck((0, 3), 'b') == False and self._isKingInCheck((0, 2), 'b') == False:  # cant castle if any of the squares are guarded!
                    legal_moves.append((0, 2))
        return legal_moves

    def pawnLegalMoves(self,color,position,recursion=False):
        """method to generate the pawns legal moves"""
        en_passant = None
        if color == 'w' and position[0] == 6:
            deltas = [[-1, 0], [-2, 0], [-1, -1], [-1, +1]]
            possible_positions = [(position[0]+i[0], position[1] + i[1]) for i in deltas]
        elif color == 'b' and position[0] == 1:
            deltas = [[+1, 0], [+2, 0], [+1, -1], [+1, +1]]
            possible_positions = [(position[0]+i[0], position[1] + i[1]) for i in deltas]
        elif color == 'w':
            deltas = [[-1, 0], [-1, -1], [-1, +1]]
            possible_positions = [(position[0]+i[0], position[1] + i[1]) for i in deltas]
        else:
            deltas = [[+1, 0], [+1, -1], [+1, +1]]
            possible_positions = [(position[0]+i[0], position[1] + i[1]) for i in deltas]
        legal_moves = []
        if position[0] == 0 or position[0] == 7:
            return legal_moves
        for i in possible_positions:
            if i[1]== -1 or i[1]==8:
                pass
            else:
                if not recursion:
                    check = self.isKingInCheck(position, i, color )
                    if recursion == False and check == True:
                        continue
                    else:
                        pass
                if position[1] - i[1] == 0 and self.board[i[0]][i[1]] == '--':
                    if abs(position[0]-i[0]) == 1:
                        legal_moves.append(i)
                    elif color == 'w' and self.board[position[0]-1][position[1]] == '--':
                        legal_moves.append(i)
                    elif color == 'b' and self.board[position[0] + 1][position[1]] == '--':
                        legal_moves.append(i)
                if position[1] - i[1] != 0 and self.board[i[0]][i[1]] != '--':
                    if self.board[i[0]][i[1]][0] != color:
                        legal_moves.append(i)
                # check for en passant
                en_passant = self.checkForEnPassant()
                if en_passant != None:
                    if en_passant in possible_positions:
                        legal_moves.append(en_passant)
        # add the legal move of en passant
        if not recursion:
            en_passant = self.checkForEnPassant()
        if not recursion and en_passant != None:
            if en_passant in possible_positions:
                legal_moves.append(en_passant)
        return legal_moves

    def checkForEnPassant(self):
        """a method to check if an en passant move is possible"""
        if len(self.moves_log) != 0:
            move = self.moves_log[-1]
        else:
            return None
        if move.pieceMoved[1] == 'P':
            if abs(move.startRow - move.endRow) == 2:
                if move.startRow == 1:
                    return (2, move.startCol)
                else:
                    return (5,move.startCol)
            else:
                return None
        else:
            return None

    def checkForPawnPromotion(self):
        """method to tell the game that a pawn is being promoted"""
        # check for pawn promotion
        for index, i in enumerate(self.board):
            for j in i:
                if j[1] == 'P' and (index == 0 or index == 7):
                    self.promotion_next = True

    def promotePawn(self, piece):
        """find all pawns and promote the one that is on the 0th or 7th row"""
        for index, i in enumerate(self.board):
            for jndex,j in enumerate(i):
                if j[1] == 'P' and (index == 0 or index == 7):
                    self.board[index][jndex] = j[0] + piece


    def queenLegalMoves(self,color,position,recursion=False):
        """method to get all the legal moves for the queen"""
        legal_moves_b = self.bishopLegalMoves(color,position,recursion)
        legal_moves_r = self.rookLegalMoves(color,position,recursion)
        legal_moves = legal_moves_r+legal_moves_b
        return legal_moves


    def knightLegalMoves(self,color,position,recursion=False):
        """method to get all the legal moves for the knight"""
        deltas = [(-2, -1), (-2, +1), (+2, -1), (+2, +1), (-1, -2), (-1, +2), (+1, -2), (+1, +2)]
        possible_positions = [(position[0] + i[0], position[1] + i[1]) for i in deltas]
        legal_moves=[]
        for i in possible_positions:
            if i[0] <0 or i[0]> 7 or i[1] < 0 or i[1]>7: #positions outside board bounds
                continue
            elif self.board[i[0]][i[1]][0] == color: #trying to take the same color
                continue
            if recursion == False:
                check = self.isKingInCheck(position, i, color)
                if recursion == False and check == True:
                    continue
                else:
                    legal_moves.append(i)
            else:
                legal_moves.append(i)
        return legal_moves

    def bishopLegalMoves(self,color,position,recursion=False):
        """method to get all the legal moves for the bischop"""
        directions = [(-1,-1),(-1,+1),(+1,-1),(+1,+1)]
        legal_moves = []
        for d in directions:
            for j in range(1,8):
                if position[0] + d[0]*j > 7 or position[0] + d[0]*j <0 or position[1] + d[1]*j > 7 or position[1] + d[1]*j <0: #out of bounds
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == color: #blocked by same color
                    break
                if recursion == False:
                    check = self.isKingInCheck(position, (position[0]+d[0]*j,position[1]+d[1]*j), color)
                    if recursion == False and check == True:
                        continue
                    else:
                        pass
                if self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == 'w' and color == 'b': #blocked by opposite color
                    legal_moves.append((position[0]+d[0]*j, position[1]+d[1]*j))
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == 'b' and color == 'w': #blocked by opposite color
                    legal_moves.append((position[0]+d[0]*j, position[1]+d[1]*j))
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j] == '--': #square is free to move onto
                    legal_moves.append((position[0] + d[0] * j, position[1] + d[1] * j))
                else:
                    break
        return legal_moves

    def rookLegalMoves(self,color,position,recursion=False):
        """method to get all the legal moves for the rook"""
        directions = [(0, -1), (0, +1), (+1, 0), (-1, 0)]
        legal_moves = []
        for d in directions:
            for j in range(1,8):
                if position[0] + d[0]*j > 7 or position[0] + d[0]*j <0 or position[1] + d[1]*j > 7 or position[1] + d[1]*j <0: #out of bounds
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == color: #blocked by same color
                    break
                if recursion == False:
                    check = self.isKingInCheck(position, (position[0]+d[0]*j,position[1]+d[1]*j), color)
                    if recursion == False and check == True:
                        continue
                    else:
                        pass
                if self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == 'w' and color == 'b': #blocked by opposite color
                    legal_moves.append((position[0]+d[0]*j, position[1]+d[1]*j))
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == 'b' and color == 'w': #blocked by opposite color
                    legal_moves.append((position[0]+d[0]*j, position[1]+d[1]*j))
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j] == '--': #square is free to move onto
                    legal_moves.append((position[0] + d[0] * j, position[1] + d[1] * j))
                else:
                    break
        return legal_moves

    def getInfluenceMoves(self,piece,startSq,recursion=False):
        """main method to collect all the moves given the type of piece, attacking own color allowed"""
        if piece[1] == 'K':
            legal_moves = self.kingInfluenceMoves(piece[0],startSq,recursion)
        elif piece[1] == 'P':
            legal_moves = self.pawnInfluenceMoves(piece[0], startSq,recursion)
        elif piece[1] == 'Q':
            legal_moves = self.queenInfluenceMoves(piece[0],startSq,recursion)
        elif piece[1] == 'N':
            legal_moves = self.knightInfluenceMoves(piece[0],startSq,recursion)
        elif piece[1] == 'B':
            legal_moves = self.bishopInfluenceMoves(piece[0],startSq,recursion)
        elif piece[1] == 'R':
            legal_moves = self.rookInfluenceMoves(piece[0],startSq,recursion)
        else:
            legal_moves = []
        return legal_moves

    def kingInfluenceMoves(self,color,position,recursion=False):
        """method to generate the kings legal moves, attacking own color allowed"""
        deltas = [(-1, -1), (-1, 0), (-1, +1), (0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1)]
        possible_positions = [(position[0]+i[0],position[1] + i[1]) for i in deltas]
        legal_moves = []
        for i in possible_positions:
            if i[0] < 0 or i[0] > 7 or i[1] < 0 or i[1] > 7: #positions outside board bounds
                pass
            else:
                legal_moves.append(i)

        # castling short and long manually
        if recursion == False and color == 'w':
            if self.w_castle_short and self.board[7][5] == '--' and self.board[7][6] == '--': # in between squares are empty and rook nor king hasntmoved
                if self._isKingInCheck((7, 4), 'w') == False and self._isKingInCheck((7, 5), 'w') == False and self._isKingInCheck((7, 6), 'w') == False: #cant castle if any of the squares are guarded!
                    legal_moves.append((7, 6))
            if self.w_castle_long and self.board[7][3] == '--' and self.board[7][2] == '--' and self.board[7][1] == '--': # in between squares are empty and rook nor king hasntmoved
                if self._isKingInCheck((7, 4), 'w') == False and self._isKingInCheck((7, 3), 'w') == False and self._isKingInCheck((7, 2), 'w') == False:  # cant castle if any of the squares are guarded!
                    legal_moves.append((7, 2))
        elif recursion == False and color == 'b':
            if self.b_castle_short and self.board[0][5] == '--' and self.board[0][6] == '--': # in between squares are empty and rook nor king hasntmoved
                if self._isKingInCheck((0, 4), 'b')== False and self._isKingInCheck((0, 5), 'b') == False and self._isKingInCheck((0,6),'b')==False: #cant castle if any of the squares are guarded!
                    legal_moves.append((0, 6))
            if self.b_castle_long and self.board[0][3] == '--' and self.board[0][2]=='--' and self.board[0][1] == '--': # in between squares are empty and rook nor king hasntmoved
                if self._isKingInCheck((0, 4), 'b') == False and self._isKingInCheck((0, 3), 'b') == False and self._isKingInCheck((0, 2), 'b') == False:  # cant castle if any of the squares are guarded!
                    legal_moves.append((0, 2))
        return legal_moves

    def pawnInfluenceMoves(self,color,position,recursion=False):
        """method to generate the pawns legal moves, attacking own color allowed, only attacking"""
        en_passant = None
        if color == 'w':
            deltas = [[-1, -1], [-1, +1]]
            possible_positions = [(position[0]+i[0], position[1] + i[1]) for i in deltas]
        else:
            deltas = [[+1, -1], [+1, +1]]
            possible_positions = [(position[0]+i[0], position[1] + i[1]) for i in deltas]
        legal_moves = []
        if position[0] == 0 or position[0] == 7:
            return legal_moves
        for i in possible_positions:
            if i[1]== -1 or i[1]==8:
                pass
            else:
                if not recursion:
                    check = self.isKingInCheck(position, i, color )
                    if recursion == False and check == True:
                        continue
                    else:
                        pass
                if position[1] - i[1] == 0 and self.board[i[0]][i[1]] == '--':
                    if abs(position[0]-i[0]) == 1:
                        legal_moves.append(i)
                    elif color == 'w' and self.board[position[0]-1][position[1]] == '--':
                        legal_moves.append(i)
                    elif color == 'b' and self.board[position[0] + 1][position[1]] == '--':
                        legal_moves.append(i)
                if position[1] - i[1] != 0 and self.board[i[0]][i[1]] != '--':
                    legal_moves.append(i)
                # check for en passant
                en_passant = self.checkForEnPassant()
                if en_passant != None:
                    if en_passant in possible_positions:
                        legal_moves.append(en_passant)
        # add the legal move of en passant
        if not recursion:
            en_passant = self.checkForEnPassant()
        if not recursion and en_passant != None:
            if en_passant in possible_positions:
                legal_moves.append(en_passant)
        return legal_moves

    def queenInfluenceMoves(self,color,position,recursion=False):
        """method to get all the legal moves for the queen, attacking own color allowed"""
        legal_moves_b = self.bishopInfluenceMoves(color,position,recursion)
        legal_moves_r = self.rookInfluenceMoves(color,position,recursion)
        legal_moves = legal_moves_r+legal_moves_b
        return legal_moves


    def knightInfluenceMoves(self,color,position,recursion=False):
        """method to get all the legal moves for the knight, attacking own color allowed"""
        deltas = [(-2, -1), (-2, +1), (+2, -1), (+2, +1), (-1, -2), (-1, +2), (+1, -2), (+1, +2)]
        possible_positions = [(position[0] + i[0], position[1] + i[1]) for i in deltas]
        legal_moves=[]
        for i in possible_positions:
            if i[0] <0 or i[0]> 7 or i[1] < 0 or i[1]>7: #positions outside board bounds
                continue
            if recursion == False:
                check = self.isKingInCheck(position, i, color)
                if recursion == False and check == True:
                    continue
                else:
                    legal_moves.append(i)
            else:
                legal_moves.append(i)
        return legal_moves

    def bishopInfluenceMoves(self,color,position,recursion=False):
        """method to get all the legal moves for the bischop, attacking own color allowed"""
        directions = [(-1,-1),(-1,+1),(+1,-1),(+1,+1)]
        legal_moves = []
        for d in directions:
            for j in range(1,8):
                if position[0] + d[0]*j > 7 or position[0] + d[0]*j <0 or position[1] + d[1]*j > 7 or position[1] + d[1]*j <0: #out of bounds
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == color: #blocked by same color
                    legal_moves.append((position[0]+d[0]*j, position[1]+d[1]*j))
                    break
                if recursion == False:
                    check = self.isKingInCheck(position, (position[0]+d[0]*j,position[1]+d[1]*j), color)
                    if recursion == False and check == True:
                        continue
                    else:
                        pass
                if self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == 'w' and color == 'b': #blocked by opposite color
                    legal_moves.append((position[0]+d[0]*j, position[1]+d[1]*j))
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == 'b' and color == 'w': #blocked by opposite color
                    legal_moves.append((position[0]+d[0]*j, position[1]+d[1]*j))
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j] == '--': #square is free to move onto
                    legal_moves.append((position[0] + d[0] * j, position[1] + d[1] * j))
                else:
                    break
        return legal_moves

    def rookInfluenceMoves(self,color,position,recursion=False):
        """method to get all the legal moves for the rook, attacking own color allowed"""
        directions = [(0, -1), (0, +1), (+1, 0), (-1, 0)]
        legal_moves = []
        for d in directions:
            for j in range(1,8):
                if position[0] + d[0]*j > 7 or position[0] + d[0]*j <0 or position[1] + d[1]*j > 7 or position[1] + d[1]*j <0: #out of bounds
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == color: #blocked by same color
                    legal_moves.append((position[0] + d[0] * j, position[1] + d[1] * j))
                    break
                if recursion == False:
                    check = self.isKingInCheck(position, (position[0]+d[0]*j,position[1]+d[1]*j), color)
                    if recursion == False and check == True:
                        continue
                    else:
                        pass
                if self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == 'w' and color == 'b': #blocked by opposite color
                    legal_moves.append((position[0]+d[0]*j, position[1]+d[1]*j))
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j][0] == 'b' and color == 'w': #blocked by opposite color
                    legal_moves.append((position[0]+d[0]*j, position[1]+d[1]*j))
                    break
                elif self.board[position[0]+d[0]*j][position[1]+d[1]*j] == '--': #square is free to move onto
                    legal_moves.append((position[0] + d[0] * j, position[1] + d[1] * j))
                else:
                    break
        return legal_moves


class Move():
    def __init__(self, startSq, endSq, board):
        """a class to represent a move that can also be logged in gamestate"""
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.board = board
        self.pieceMoved = board[self.startRow,self.startCol]
        self.pieceCaptured = board[self.endRow,self.endCol]
        # map the row to ranks and  files to cols
        self.ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                       "5": 3, "6": 2, "7": 1, "8": 0}
        self.rowsToRanks = {v: k for k, v in self.ranksToRows.items()}
        self.filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                       "e": 4, "f": 5, "g": 6, "h": 7}
        self.colsToFiles = {v: k for k, v in self.filesToCols.items()}
        """information to find out if castling was legit prior to this move"""
        self.w_castle_short = True
        self.w_castle_long = True
        self.b_castle_short = True
        self.b_castle_long = True
        self.w_castle_this_move_short = False
        self.w_castle_this_move_long = False
        self.b_castle_this_move_short = False
        self.b_castle_this_move_long = False
        self.enpassantmove = False
        self.none_captured = None
        self.bk_in_check = False
        self.wk_in_check = False

    def getChessNotation(self):
        """method to get the chess notation of a move"""
        #have to add castles, checks, promotion and notation for when multiple moves fit the basic notation
        if self.pieceCaptured != "--":
            captured = 'x'
        else:
            captured = ''
        if self.pieceMoved[1]!= 'P':
            return self.pieceMoved[1] + captured + self.getRankFile(self.endRow, self.endCol)
        else:
            return captured + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r,c):
        """helping method to numerise the ranks and files"""
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def set_kings_in_check(self, color, bool):
        if color == 'b':
            self.bk_in_check = bool
        else:
            self.wk_in_check = bool
"""
responsable for handling the bots moves
"""
import random
from Data import Engine
import copy
import math
import numpy as np


class Computer():
    def __init__(self, color, depth):
        self.board_evaluation = 0
        self.color = color
        self.depth = depth
        self.depth_counter = 0
        if self.color == 'b':
            self.player_color = 'w'
        else:
            self.player_color = 'b'

        self.pawn_value_multiplier_b = np.array([
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.8, 0.9, 1.0, 1.1, 1.1, 1.0, 0.9, 0.8],
            [0.9, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 0.9],
            [1.0, 1.1, 1.2, 1.3, 1.3, 1.2, 1.1, 1.0],
            [1.1, 1.2, 1.3, 1.4, 1.4, 1.3, 1.2, 1.1],
            [1.3, 1.4, 1.5, 1.6, 1.6, 1.5, 1.4, 1.3],
            [1.5, 1.6, 1.7, 1.8, 1.8, 1.7, 1.6, 1.5],
            [9, 9, 9, 9, 9, 9, 9, 9],
        ])
        self.pawn_value_multiplier_w = np.array([
            [9, 9, 9, 9, 9, 9, 9, 9],
            [1.5, 1.6, 1.7, 1.8, 1.8, 1.7, 1.6, 1.5],
            [1.3, 1.4, 1.5, 1.6, 1.6, 1.5, 1.4, 1.3],
            [1.1, 1.2, 1.3, 1.4, 1.4, 1.3, 1.2, 1.1],
            [1.0, 1.1, 1.2, 1.3, 1.3, 1.2, 1.1, 1.0],
            [0.9, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 0.9],
            [0.8, 0.9, 1.0, 1.1, 1.1, 1.0, 0.9, 0.8],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ])
        self.knight_value_multiplier = np.array([
            [0.4, 0.6, 0.8, 0.8, 0.8, 0.8, 0.6, 0.4],
            [0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 0.8, 0.6],
            [0.8, 1.0, 1.2, 1.2, 1.2, 1.2, 1.0, 0.8],
            [0.8, 1.0, 1.2, 1.2, 1.2, 1.2, 1.0, 0.8],
            [0.8, 1.0, 1.2, 1.2, 1.2, 1.2, 1.0, 0.8],
            [0.8, 1.0, 1.2, 1.2, 1.2, 1.2, 1.0, 0.8],
            [0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 0.8, 0.6],
            [0.4, 0.6, 0.8, 0.8, 0.8, 0.8, 0.6, 0.4],
        ])
        self.bishop_value_multiplier = np.array([
            [1.0, 0.6, 0.6, 0.8, 0.8, 0.6, 0.6, 1.0],
            [0.6, 1.3, 1.0, 1.0, 1.0, 1.0, 1.3, 0.6],
            [0.8, 1.0, 1.2, 1.1, 1.1, 1.2, 1.0, 0.8],
            [0.8, 1.0, 1.1, 1.1, 1.1, 1.1, 1.0, 0.8],
            [0.8, 1.0, 1.1, 1.1, 1.1, 1.1, 1.0, 0.8],
            [0.8, 1.0, 1.2, 1.1, 1.1, 1.2, 1.0, 0.8],
            [0.6, 1.3, 1.0, 1.0, 1.0, 1.0, 1.3, 0.6],
            [1.0, 0.6, 0.6, 0.8, 0.8, 0.6, 0.6, 1.0],
        ])
        self.rook_value_multiplier_b = np.array([
            [0.95, 1.0, 1.0, 1.05, 1.0, 1.05, 1.0, 0.95],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        ])
        self.rook_value_multiplier_w = np.array([
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [0.95, 1.0, 1.0, 1.05, 1.0, 1.05, 1.0, 0.95],
        ])
        self.king_value_multiplier = np.array([
            [1.0, 1.0, 1.1, 0.90, 1.0, 0.90, 1.1, 1.0],
            [1.0, 1.0, 1.0, 0.95, 0.95, 0.95, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 0.95, 1.0, 0.95, 1.0, 1.0],
            [1.0, 1.0, 1.1, 0.90, 1.0, 0.90, 1.1, 1.0],
        ])
        self.queen_value_multiplier = np.array([
            [1.0, 1.0, 1.0, 0.95, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.01, 1.02, 1.03, 1.03, 1.02, 1.01, 1.0],
            [1.01, 1.02, 1.03, 1.04, 1.04, 1.03, 1.02, 1.01],
            [1.01, 1.02, 1.03, 1.04, 1.04, 1.03, 1.02, 1.01],
            [1.01, 1.02, 1.03, 1.04, 1.04, 1.03, 1.02, 1.01],
            [1.01, 1.02, 1.03, 1.04, 1.04, 1.03, 1.02, 1.01],
            [1.0, 1.01, 1.02, 1.03, 1.03, 1.02, 1.01, 1.0],
            [1.0, 1.0, 1.0, 0.95, 1.0, 1.0, 1.0, 1.0],
        ])
        self.current_gamestate_evaluation = 0

    def find_all_legal_moves(self, gamestate, t_color, matrix= None):
        all_possible_moves = []
        values = {'P' : 1, 'Q' : 9, 'R' : 5, 'N' : 3, 'B' : 3 , '-' : 0, 'K' : 0}
        for i in range(8):
            for j in range(8):
                if gamestate.board[i][j][0] !=t_color:
                    pass
                else:
                    piece = gamestate.board[i][j]
                    start_sq = (i, j)
                    legal_moves = gamestate.getLegalMoves(piece, start_sq)
                    if len(legal_moves) > 0:
                        for k in legal_moves:
                            end_sq = k
                            target_piece = gamestate.board[end_sq[0]][end_sq[1]]
                            if  piece[1] == 'P' or values[piece[1]] <= values[target_piece[1]] or target_piece[1] == '-' or (matrix[end_sq[0]][end_sq[1]] > 0): #TODO check the total value your attacking and attacking with, if your attacking value is lowe, overwrite the move with this move tow in material
                                move = (start_sq,end_sq)
                                all_possible_moves.append(move)
        return all_possible_moves

    def get_influence_matrix(self, gamestate):
        """method to get influence per square, positive is bot influence, negative is players"""
        i_matrix = np.zeros([8,8])
        for i in range(8):
            for j in range(8):
                piece = gamestate.board[i][j]
                start_sq = (i, j)
                influence_moves = gamestate.getInfluenceMoves(piece, start_sq)
                if len(influence_moves) > 0:
                    for k in influence_moves:
                        if piece[0] == self.color:
                            i_matrix[k[0],k[1]] += 1
                        else:
                            i_matrix[k[0], k[1]] -= 1
        print(i_matrix)
        return i_matrix

    def analyse_control(self, matrix):
        """method to analyse who has more control over a square, positive means the bot has more control"""
        boardcontrol = np.sum(matrix > 0) - np.sum(matrix < 0)
        return boardcontrol

    def make_random_move(self, gamestate):
        move_start_end = random.choice(self.all_possible_moves)
        move_start = move_start_end[0]
        move_end = move_start_end[1]
        piece = gamestate.board[move_start[0]][move_start[1]]
        move = Engine.Move(move_start, move_end, gamestate.board)
        return move

    def evaluate_boardstate_new(self, gamestate):
        ## COLOR is bot color
        board_evaluation = 0
        checkmate = False
        if gamestate.wK_incheck or gamestate.bK_incheck:
            checkmate = gamestate.checkForCheckmate()
        if checkmate and gamestate.wK_incheck:
            if self.color == 'b':
                board_evaluation = 9999
            else:
                board_evaluation = -9999
        elif checkmate:
            if self.color == 'w':
                board_evaluation = 9999
            else:
                board_evaluation = -9999
        else:
            #### calc material difference, negative means the player has better material
            material_difference = self._calc_material_difference(gamestate)
            #### calc the control over the board
            influence_matrix = self.get_influence_matrix(gamestate)
            control = self.analyse_control(influence_matrix)
            board_evaluation = material_difference + control *0.1

        return board_evaluation

    def _calc_material_difference(self, gamestate):
        """method to calc the material difference, where pawns can be worth a lot more if they are passed or connected, color is botcolor"""
        player_material = 0
        bot_material = 0
        for i in range(8):
            for j in range(8):
                ##### add to the boardstate if the color is the  bot color
                if gamestate.board[i][j][0] == self.color:
                    if gamestate.board[i][j][1] == 'Q':
                        bot_material += 9
                    elif gamestate.board[i][j][1] == 'R':
                        # TODO this wont work with making the bot white, if we ever want to do that
                        bot_material += 5 * self.rook_value_multiplier_b[i][j]
                    elif gamestate.board[i][j][1] == 'N':
                        bot_material += 3 * self.knight_value_multiplier[i][j]
                    elif gamestate.board[i][j][1] == 'B':
                        bot_material += 3 * self.bishop_value_multiplier[i][j]
                    elif gamestate.board[i][j][1] == 'P':
                        if 0 < j < 7:
                            # TODO this wont work with making the bot white, if we ever want to do that
                            if gamestate.board[i - 1][j - 1] == 'bP' or gamestate.board[i - 1][j + 1] == 'bP':
                                pawn_chain_multiplier = 1.25
                            elif gamestate.board[i - 1][j] == 'bP':
                                pawn_chain_multiplier = 0.75
                            else:
                                pawn_chain_multiplier = 1
                        elif gamestate.board[i - 1][j] == 'bP':
                            pawn_chain_multiplier = 0.75
                        else:
                            pawn_chain_multiplier = 1
                        ### check for passed pawns
                        if 0 < j < 7:
                            if "wP" not in (gamestate.board[:, j]) and "wP" not in (
                            gamestate.board[:, j - 1]) and "wP" not in (gamestate.board[:, j + 1]):
                                pawn_chain_multiplier = 2
                        elif j == 0:
                            if "wP" not in (gamestate.board[:, j]) and "wP" not in (gamestate.board[:, j + 1]):
                                pawn_chain_multiplier = 2
                        else:
                            if "wP" not in (gamestate.board[:, j]) and "wP" not in (gamestate.board[:, j - 1]):
                                pawn_chain_multiplier = 2
                        bot_material += 1 * self.pawn_value_multiplier_b[i][j] * pawn_chain_multiplier
                    elif gamestate.board[i][j][1] == 'K':
                        if len(gamestate.moves_log) < 20:  # if in the first 30 moves
                            bot_material += 10 * self.king_value_multiplier[i][j]
                        else:
                            bot_material += 10
                ###### and substract if the color is that of the player
                elif gamestate.board[i][j][0] != '-':
                    if gamestate.board[i][j][1] == 'Q':
                        player_material += 9
                    elif gamestate.board[i][j][1] == 'R':
                        player_material += 5 * self.rook_value_multiplier_w[i][j]
                    elif gamestate.board[i][j][1] == 'N':
                        player_material += 3 * self.knight_value_multiplier[i][j]
                    elif gamestate.board[i][j][1] == 'B':
                        player_material += 3 * self.bishop_value_multiplier[i][j]
                    elif gamestate.board[i][j][1] == 'P':
                        if 0 < j < 7:
                            if gamestate.board[i + 1][j - 1] == 'wP' or gamestate.board[i + 1][j + 1] == 'wP':
                                pawn_chain_multiplier = 1.25
                            elif gamestate.board[i + 1][j] == 'wP':
                                pawn_chain_multiplier = 0.75
                            else:
                                pawn_chain_multiplier = 1
                        elif gamestate.board[i + 1][j] == 'wP':
                            pawn_chain_multiplier = 0.75
                        else:
                            pawn_chain_multiplier = 1
                        ### check for passed pawns
                        if 0 < j < 7:
                            if "bP" not in (gamestate.board[:, j]) and "bP" not in (
                            gamestate.board[:, j - 1]) and "bP" not in (gamestate.board[:, j + 1]):
                                pawn_chain_multiplier = 2
                        elif j == 0:
                            if "bP" not in (gamestate.board[:, j]) and "bP" not in (gamestate.board[:, j + 1]):
                                pawn_chain_multiplier = 2
                        else:
                            if "bP" not in (gamestate.board[:, j]) and "bP" not in (gamestate.board[:, j - 1]):
                                pawn_chain_multiplier = 2
                        player_material += 1 * self.pawn_value_multiplier_w[i][j] * pawn_chain_multiplier
                    elif gamestate.board[i][j][1] == 'K':
                        if len(gamestate.moves_log) < 20:  # if in the first 30 moves
                            player_material += 10 * self.king_value_multiplier[i][j]
                        else:
                            player_material += 10
        #### add a bonus for material difference, since that is typically the most important, especially for a bot
        return bot_material - player_material

    def min_max_gamestate(self, gs, gs_small):
        if gs.depth < self.depth:
            if gs_small.depth % 2 == 1:
                t_color = self.color
            else:
                t_color = self.player_color
            ##### first find all possible moves
            gs_small.influence_matrix = self.get_influence_matrix(gs)
            gs_small.all_possible_moves = self.find_all_legal_moves(gs, t_color, gs_small.influence_matrix)
            ##### give an evaluation of 0 if len moves is 0
            if len(gs_small.all_possible_moves) == 0:
                print("the problem lies here")
                if gs.checkForCheckmate():
                    if t_color == self.player_color:
                        gs_small.evaluation = 9999
                    else:
                        gs_small.evaluation = -9999
                else:
                    gs_small.evaluation = -1000
            ##### if not check mate start the min max algorithm by making every move untill the specified depth is found
            else:
                for i in gs_small.all_possible_moves:
                    #### apha beta pruning only make move if a better option can still be found
                    if gs_small.parent_gs != None:
                        if  len(gs_small.parent_gs.child_evaluations)  > 0 and len(gs_small.child_evaluations) > 0:
                            if gs_small.child_evaluations != None and gs_small.parent_gs.child_evaluations != None:
                                if gs_small.depth % 2 == 1:
                                    if max(gs_small.child_evaluations) > min(gs_small.parent_gs.child_evaluations):
                                        print("we are actually reaching this condition!!")
                                        break
                                else:
                                    if min(gs_small.child_evaluations) < max(gs_small.parent_gs.child_evaluations):
                                        print("we are actually reaching this condition!!")
                                        break
                    ###### make the move
                    move_start = i[0]
                    move_end = i[1]
                    move = Engine.Move(move_start, move_end, gs.board)
                    gs.makeMove(move, True)
                    ##### make new small gamestate to capture all the info
                    if gs_small.depth +1 != self.depth: # only go deeper if the depth is not yet reached
                        new_gs_small = SmallGs(gs_small, gs_small.depth + 1)
                        ##### recursive min max
                        self.min_max_gamestate(gs, new_gs_small)
                        ##### min max the value based on all the child evaluations of the small gamestate
                        ##### ALSO add the possible moves to the outcome
                        if gs_small.depth % 2 == 0:
                            if len(new_gs_small.child_evaluations) > 0:
                                new_gs_small.evaluation = max(new_gs_small.child_evaluations)
                        else:
                            if len(new_gs_small.child_evaluations) > 0:
                                new_gs_small.evaluation = min(new_gs_small.child_evaluations)
                        #### append the newfound evaluation to the parents child_evalutaion (only if it has a parent)
                        #new_gs_small.best_move_from_here = new_gs_small.child_moves[new_gs_small.best_move_index]
                        if new_gs_small.parent_gs != None:
                            new_gs_small.parent_gs.child_evaluations.append(new_gs_small.evaluation)
                    else: # this is what happens if the bottom is reached, the gamestate is actually evaluated
                        ####### possible alpha beta pruning
                        if gs_small.depth % 2 == 1:
                            if len(gs_small.child_evaluations) > 0 and len(gs_small.parent_gs.child_evaluations) > 0:
                                if max(gs_small.child_evaluations) > min(
                                        gs_small.parent_gs.child_evaluations):  # alphabeta pruning
                                    print("we are actually reaching this even deeper condition!!")
                                    pass
                                else:
                                    evaluation = self.evaluate_boardstate_new(gs)
                                    gs_small.child_evaluations.append(evaluation)
                            else:
                                evaluation = self.evaluate_boardstate_new(gs)
                                gs_small.child_evaluations.append(evaluation)
                        else:
                            if len(gs_small.child_evaluations) > 0 and len(gs_small.parent_gs.child_evaluations) >0:
                                if min(gs_small.child_evaluations) < max(gs_small.parent_gs.child_evaluations): #alphabeta pruning
                                    print("we are actually reaching this even deeper condition!!")
                                    pass
                                else:
                                    evaluation = self.evaluate_boardstate_new(gs)
                                    gs_small.child_evaluations.append(evaluation)
                            else:
                                evaluation = self.evaluate_boardstate_new(gs)
                                gs_small.child_evaluations.append(evaluation)
                    ##### dont forget to undo the move
                    gs.undoMove()
                if gs_small.depth == 1:
                    ##### set the best move index to be retrieved
                    gs_small.best_move_index = gs_small.child_evaluations.index(max(gs_small.child_evaluations))
        else:
            pass

    def make_best_move(self, gs):
        # TODO if you can castle force it
        gs_copy = copy.deepcopy(gs)
        gs_small = SmallGs(None, 1)
        self.min_max_gamestate(gs_copy, gs_small)
        print("best move evaluation:", max(gs_small.child_evaluations))
        print(len(gs_small.child_evaluations), len(gs_small.all_possible_moves))
        index = gs_small.best_move_index
        matrix = self.get_influence_matrix(gs)
        all_possible_moves = self.find_all_legal_moves(gs, self.color, matrix)
        move_start = all_possible_moves[index][0]
        move_end = all_possible_moves[index][1]
        best_move = Engine.Move(move_start, move_end, gs.board)
        # set depth 1 lower if checkmate sequence is found
        if self.depth > 1 and gs_small.evaluation == 9999:
            self.depth -= 1
        return best_move

class SmallGs():
    def __init__(self, parent_gs, depth):
        self.evaluation = None
        self.influence_matrix = None
        self.parent_gs = parent_gs
        self.child_gs = []
        self.depth = depth
        self.best_move_index = None
        self.child_evaluations = []
        self.all_possible_moves = []

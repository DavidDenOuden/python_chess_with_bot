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
        self.moves_considered = 0
        if self.color == 'b':
            self.player_color = 'w'
        else:
            self.player_color = 'b'

        self.matrixes_updated = False
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
            [0.7, 0.8, 0.9, 0.9, 0.9, 0.9, 0.8, 0.7],
            [0.8, 0.8, 1.0, 1.0, 1.0, 1.0, 0.9, 0.7],
            [0.9, 1.0, 1.02, 1.0, 1.0, 1.02, 1.0, 0.9],
            [0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9],
            [0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9],
            [0.9, 1.0, 1.02, 1.0, 1.0, 1.02, 1.0, 0.9],
            [0.8, 0.8, 1.0, 1.0, 1.0, 1.0, 0.9, 0.8],
            [0.7, 0.8, 1.0, 1.0, 1.0, 1.0, 0.9, 0.7],
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
            [1, 1.0, 1.0, 1.05, 1.0, 1.05, 1.0, 1],
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
            [1, 1.0, 1.0, 1.05, 1.0, 1.05, 1.0, 1],
        ])
        self.king_value_multiplier = np.array([
            [1.0, 1.0, 1.01, 0.90, 1.0, 0.90, 1.01, 1.0],
            [1.0, 1.0, 1.0, 0.95, 0.95, 0.95, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 0.95, 1.0, 0.95, 1.0, 1.0],
            [1.0, 1.0, 1.01, 0.90, 1.0, 0.90, 1.01, 1.0],
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
                            #if  piece[1] == 'P' or values[piece[1]] <= values[target_piece[1]] or target_piece[1] == '-' or (matrix[end_sq[0]][end_sq[1]] > 0):
                            move = (start_sq,end_sq)
                            all_possible_moves.append(move)
        return all_possible_moves

    def get_influence_matrix(self, gamestate):
        """method to get influence per square, positive is bot influence, negative is players"""
        values = {'P': 1, 'Q': 9, 'R': 5, 'N': 3, 'B': 3, '-': 0, 'K': 0}
        i_matrix = np.zeros([8,8])
        iv_matrix = np.zeros([8, 8])
        rv_matrix = np.zeros([8, 8])
        bot_pawn_influence_matrix = np.zeros([8, 8])
        player_pawn_influence_matrix = np.zeros([8, 8])
        for i in range(8):
            for j in range(8):
                piece = gamestate.board[i][j]
                if piece[0] == self.color:
                    rv_matrix[i, j] += values[piece[1]]
                elif piece[0] != '-':
                    rv_matrix[i, j] -= values[piece[1]]
                start_sq = (i, j)
                influence_moves = gamestate.getInfluenceMoves(piece, start_sq)
                if len(influence_moves) > 0:
                    for k in influence_moves:
                        if piece[0] == self.color:
                            i_matrix[k[0], k[1]] += 1
                            iv_matrix[k[0], k[1]] += values[piece[1]]
                            if piece[1]=='P':
                                bot_pawn_influence_matrix[k[0], k[1]] = 1
                        elif piece[1] != '-':
                            i_matrix[k[0], k[1]] -= 1
                            iv_matrix[k[0], k[1]] -= values[piece[1]]
                            if piece[1]=='P':
                                player_pawn_influence_matrix[k[0], k[1]] = 1
        #print(i_matrix)
        #print(iv_matrix)
        #print(rv_matrix)
        #print(bot_pawn_influence_matrix)
        return (i_matrix,iv_matrix,rv_matrix,bot_pawn_influence_matrix,player_pawn_influence_matrix)

    def analyse_control(self, matrix):
        """method to analyse who has more control over a square, positive means the bot has more control"""
        boardcontrol = np.sum(matrix > 0) - np.sum(matrix < 0)
        return boardcontrol

    def identify_weakspots(self, i_matrix, iv_matrix, rv_matrix, bp_matrix, pp_matrix):
        """method to identify if there are any spots where material loss is evident, punishment negative means its not good for the bot, if its positive it means its not good for the player"""
        punishment = 0
        two_aggro_moves = False
        for row in range(8):
            for column in range(8):
                if (i_matrix[row][column] < 0 and rv_matrix[row][column] > 0) :#and (abs(iv_matrix[row][column]) <= abs(rv_matrix[row][column])):
                    # add a punishment if your piece is unsufficiently defended
                    punishment -= abs(rv_matrix[row][column]) *0.44
                elif (i_matrix[row][column] > 0 and rv_matrix[row][column] < 0) :#and abs(iv_matrix[row][column]) <= abs(rv_matrix[row][column]):
                    # add a punishment if your piece is unsufficiently defended
                    punishment += abs(rv_matrix[row][column]) *0.44
                elif bp_matrix[row][column] > 0 and rv_matrix[row][column] < -1: #pawn aggro move
                    punishment += abs(rv_matrix[row][column]) * 1 *0.44
                elif pp_matrix[row][column] > 0 and rv_matrix[row][column] > 1: #pawn aggro move
                    punishment -= abs(rv_matrix[row][column]) * 1 *0.44
        if punishment != 0:
            print("THERES PUNISHMENT AND ITS", punishment)
        return punishment

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
                print("BOARD EVALUTATION TO -9999")
        else:
            #### calc material difference, negative means the player has better material
            material_difference = self._calc_material_difference(gamestate)
            #### calc the control over the board
            matrix_tuple = self.get_influence_matrix(gamestate)
            influence_matrix, ivalue_matrix, realvalue_matrix, bp_matrix, pp_matrix = matrix_tuple[0], matrix_tuple[1], matrix_tuple[2], matrix_tuple[3], matrix_tuple[4]
            control = self.analyse_control(influence_matrix)
            punishment = self.identify_weakspots(influence_matrix,ivalue_matrix,realvalue_matrix, bp_matrix, pp_matrix)
            board_evaluation = material_difference *2 + control *0.1 + punishment

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
                                pawn_chain_multiplier = 0.9
                            else:
                                pawn_chain_multiplier = 1
                        elif j == 0:
                            if gamestate.board[i - 1][j + 1] == 'bP':
                                pawn_chain_multiplier = 1.25
                            elif gamestate.board[i - 1][j] == 'bP':
                                pawn_chain_multiplier = 0.9
                            else:
                                pawn_chain_multiplier = 1
                        else:
                            if gamestate.board[i - 1][j - 1] == 'bP':
                                pawn_chain_multiplier = 1.25
                            elif gamestate.board[i - 1][j] == 'bP':
                                pawn_chain_multiplier = 0.9
                            else:
                                pawn_chain_multiplier = 1
                        ### check for passed pawns
                        if 0 < j < 7:
                            if "wP" not in (gamestate.board[:, j]) and "wP" not in (
                            gamestate.board[:, j - 1]) and "wP" not in (gamestate.board[:, j + 1]):
                                pawn_chain_multiplier *= 2
                        elif j == 0:
                            if "wP" not in (gamestate.board[:, j]) and "wP" not in (gamestate.board[:, j + 1]):
                                pawn_chain_multiplier *= 2
                        else:
                            if "wP" not in (gamestate.board[:, j]) and "wP" not in (gamestate.board[:, j - 1]):
                                pawn_chain_multiplier *= 2
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
                            # TODO this wont work with making the bot white, if we ever want to do that
                            if gamestate.board[i + 1][j - 1] == 'wP' or gamestate.board[i + 1][j + 1] == 'wP':
                                pawn_chain_multiplier = 1.25
                            elif gamestate.board[i - 1][j] == 'wP':
                                pawn_chain_multiplier = 0.9
                            else:
                                pawn_chain_multiplier = 1
                        elif j == 0:
                            if gamestate.board[i + 1][j + 1] == 'wP':
                                pawn_chain_multiplier = 1.25
                            elif gamestate.board[i + 1][j] == 'wP':
                                pawn_chain_multiplier = 0.9
                            else:
                                pawn_chain_multiplier = 1
                        else:
                            if gamestate.board[i + 1][j - 1] == 'wP':
                                pawn_chain_multiplier = 1.25
                            elif gamestate.board[i + 1][j] == 'wP':
                                pawn_chain_multiplier = 0.9
                            else:
                                pawn_chain_multiplier = 1
                        ### check for passed pawns
                        if 0 < j < 7:
                            if "bP" not in (gamestate.board[:, j]) and "bP" not in (
                            gamestate.board[:, j - 1]) and "bP" not in (gamestate.board[:, j + 1]):
                                pawn_chain_multiplier *= 2
                        elif j == 0:
                            if "bP" not in (gamestate.board[:, j]) and "bP" not in (gamestate.board[:, j + 1]):
                                pawn_chain_multiplier *= 2
                        else:
                            if "bP" not in (gamestate.board[:, j]) and "bP" not in (gamestate.board[:, j - 1]):
                                pawn_chain_multiplier *= 2
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
            gs_small.influence_matrix = self.get_influence_matrix(gs)[0]
            gs_small.all_possible_moves = self.find_all_legal_moves(gs, t_color, gs_small.influence_matrix)
            self.moves_considered += len(gs_small.all_possible_moves)
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
        self.update_depth(gs)
        if len(gs.moves_log) > 30 and self.matrixes_updated == False:
            self.update_matrix()
        gs_copy = copy.deepcopy(gs)
        gs_small = SmallGs(None, 1)
        self.min_max_gamestate(gs_copy, gs_small)
        print("best move evaluation:", max(gs_small.child_evaluations))
        print("moves considered:", self.moves_considered)
        print(len(gs_small.child_evaluations), len(gs_small.all_possible_moves))
        index = gs_small.best_move_index
        matrix = self.get_influence_matrix(gs)[0]
        all_possible_moves = self.find_all_legal_moves(gs, self.color, matrix)
        move_start = all_possible_moves[index][0]
        move_end = all_possible_moves[index][1]
        best_move = Engine.Move(move_start, move_end, gs.board)
        # set depth 1 lower if checkmate sequence is found
        if self.depth > 1 and gs_small.evaluation == 9999:
            self.depth -= 1
        return best_move

    def update_depth(self, gs):
        """function to make the computer smarter if theres room for it"""
        values = {'P': 1, 'Q': 9, 'R': 5, 'N': 3, 'B': 3, '-': 0, 'K': 3}
        total_value = 0
        for row in range(8):
            for column in range(8):
                total_value += values[gs.board[row][column][1]]
        if total_value < 15:
            self.depth = 5
        elif total_value < 27:
            self.depth = 4
        else:
            self.depth = 3

    def update_matrix(self):
        """function to update the matrix once move 20 is hit (or 10 per side)"""
        print("UPDATED MATRIX")
        print("UPDATED MATRIX")
        print("UPDATED MATRIX")
        print("UPDATED MATRIX")
        print("UPDATED MATRIX")
        print("UPDATED MATRIX")
        print("UPDATED MATRIX")
        print("UPDATED MATRIX")

        self.matrixes_updated = True
        self.knight_value_multiplier = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ])
        self.bishop_value_multiplier = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ])
        self.rook_value_multiplier_b = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ])
        self.rook_value_multiplier_w = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02, 1.02],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ])
        self.king_value_multiplier = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ])
        self.queen_value_multiplier = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ])

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

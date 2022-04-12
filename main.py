"""
Main file that runs the game, displays the game and handles user input
"""

import pygame as p
from Data import Engine, Bot
import os
import numpy as np

print('hi')
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
SELECTED = p.transform.scale(p.image.load(os.path.join("Data", "graphics", "selected.png")), (SQ_SIZE, SQ_SIZE))
LEGAL_MOVES = p.transform.scale(p.image.load(os.path.join("Data", "graphics", "legal_moves.png")), (SQ_SIZE, SQ_SIZE))
CHECKMATE = p.transform.scale(p.image.load(os.path.join("Data", "graphics", "checkmate.png")), (SQ_SIZE * 4, SQ_SIZE))
PAWNPROMOTION = p.image.load(os.path.join("Data", "graphics", "pawn_promotion.png"))
KINGINCHECK = p.transform.scale(p.image.load(os.path.join("Data", "graphics", "king_in_check.png")), (SQ_SIZE, SQ_SIZE))
DRAW = p.transform.scale(p.image.load(os.path.join("Data", "graphics", "draw.png")), (SQ_SIZE * 2, SQ_SIZE))
PLAYERCOLOR = 'w'
BOTCOLOR = 'b'

bot = Bot.Computer(BOTCOLOR, 3)

def loadImages():
    """load the images"""
    pieces = ["bQ", "bK", "bB", "bN", "bR","wQ", "wK", "wB", "wN", "wR", "bP", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(os.path.join("Data", "images", piece + ".png")), (SQ_SIZE, SQ_SIZE))



def main():
    """Main solver for code that handles the input and draws the gamestate"""
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    gs = Engine.GameState()
    loadImages()
    p.display.set_icon(IMAGES["bN"])
    running = True
    sqSelected = () # no square selected by default keep track of last click tuple(row,col)
    playerClicks = [] #keep track of player clicks (two tuples)
    legal_moves = None
    checkmate = False
    check = False
    draw = False
    pawnpromotion = False
    counter = 0

    while running:
        ###pawn promotion check###
        if gs.promotion_next:
            pawnpromotion = True

        ###check check###
        if gs.white_to_move:
            color_to_move = 'w'
        else:
            color_to_move = 'b'
        if gs.isKingInCheck((0, 0), (0, 0), color_to_move):
            check = True

        ###checkmate check###
        checkmate = gs.checkForCheckmate()

        ###draw check###
        if not checkmate and gs.checkForStalemate(): #check if there is a stalemate situation
            draw = True
            print("stalemate")
        if gs.checkForDrawRepitition(): # check if the game should be drawn by 3 fold repetition.
            draw = True
        elif gs.none_captured == 100: # check if the game should end in a draw since no pieces were captured or pawns were moved
            draw = True

        ###drawing gamestate and resetting booleans###
        drawGameState(screen, gs, sqSelected,legal_moves,checkmate,pawnpromotion, check, color_to_move,draw) #show peces, selected piece, and legal moves
        pawnpromotion = False
        check = False
        clock.tick(MAX_FPS)
        p.display.flip()

        #check if the player or bot has to move
        if gs.white_to_move:
            if PLAYERCOLOR == 'w':
                player_to_move = True
            else:
                player_to_move = False
        else:
            if PLAYERCOLOR == 'b':
                player_to_move = True
            else:
                player_to_move = False

        ###game handle on promotion###
        if gs.promotion_next:
            if not player_to_move:
                for e in p.event.get(): #get input from player
                    if e.type == p.QUIT:
                        running = False
                    # show choices on screen
                    if counter == 0: # only print the first time
                        print('choose promotion, press 1 for Q, 2 for R, 3 for B and 4 for N')
                        counter = 1
                    if e.type == p.KEYDOWN:
                        if e.key == p.K_1:
                            gs.promotePawn('Q')
                            gs.promotion_next = False
                        elif e.key == p.K_2:
                            gs.promotePawn('R')
                            gs.promotion_next = False
                        elif e.key == p.K_3:
                            gs.promotePawn('B')
                            gs.promotion_next = False
                        elif e.key == p.K_4:
                            gs.promotePawn('N')
                            gs.promotion_next = False
            else: #automatic promote to queen
                gs.promotePawn('Q')
                gs.promotion_next = False

        ###game handle on checkmate###
        if checkmate: # cancel all other options if the game is drawn
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

        ###game handle on draw###
        elif draw: # cancel all other options if the game is drawn
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

        ###game handle in all other cases###
        else:
            if player_to_move:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif e.type == p.MOUSEBUTTONDOWN:
                        counter = 0 # reset printing for promotion
                        if e.button == 1:

                            ###select or deselect a piece###
                            if len(playerClicks) < 2:
                                location = p.mouse.get_pos() #(x,y) location of the mouse
                                start_col = location[0]//SQ_SIZE
                                start_row = location[1]//SQ_SIZE
                                sqSelected = (start_row,start_col)
                                if len(playerClicks) == 0: #check for legal moves
                                    piece_selected = gs.board[start_row][start_col]
                                    ###make sure that the correct color is about to move###
                                    if gs.white_to_move == True:
                                        if piece_selected[0] == 'w':
                                            correct_color = True
                                        else:
                                            correct_color = False
                                            sqSelected = ()
                                    else:
                                        if piece_selected[0] == 'b':
                                            correct_color = True
                                        else:
                                            correct_color = False
                                            sqSelected = ()
                                    if correct_color:
                                        legal_moves = gs.getLegalMoves(piece_selected, (start_row, start_col)) # get legal moves
                                        playerClicks.append(sqSelected) # append first click
                                elif len(playerClicks) == 1:
                                    if (start_row,start_col) not in legal_moves: # user does not click on legal move second time!
                                        sqSelected = () # unselect
                                        playerClicks = []
                                        legal_moves = []
                                    else:
                                        sqSelected = (start_row, start_col)
                                        playerClicks.append(sqSelected) # append second click
                            ###register the second click as the move to be made and make the move###
                            if len(playerClicks) == 2:
                                move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                                print(move.getChessNotation())
                                gs.makeMove(move,True)
                                gs.checkForPawnPromotion()
                                sqSelected = ()
                                playerClicks = []
                                legal_moves = []
                        elif e.button == 3: #rmb is clicked
                            if len(playerClicks) != 0:
                                sqSelected = () #clear selected
                                playerClicks = [] #clear all lmb clicks
                            elif not gs.promotion_next:
                                gs.undoMove()

            ###handle bot moves###
            else:
                move = bot.make_best_move(gs)
                gs.makeMove(move, True)
                gs.checkForPawnPromotion()
                evaluation = bot.evaluate_boardstate_new(gs)
                print(evaluation)


def drawGameState(screen, gs,sqSelected=None, legalSqs = None, checkmate=False, pawn_promotion = False, check = False, color_to_move ='w', draw = False):
    """main function to be able to draw a gamestate, calls all other draw functions"""
    drawBoard(screen) #draw squares
    if sqSelected != ():
        drawSelected(screen, sqSelected)
    if check and color_to_move == 'w':
        screen.blit(KINGINCHECK, p.Rect(gs.wK_pos[1] * SQ_SIZE, gs.wK_pos[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    elif check and color_to_move == 'b':
        screen.blit(KINGINCHECK, p.Rect(gs.bK_pos[1] * SQ_SIZE, gs.bK_pos[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    drawPieces(screen, gs.board) #draw pieces
    if legalSqs != None:
        drawLegalMoves(screen,legalSqs)
    if checkmate:
        screen.blit(CHECKMATE, p.Rect(2 * SQ_SIZE, 3.5 * SQ_SIZE, 4*SQ_SIZE, SQ_SIZE))
    if draw and not checkmate:
        screen.blit(DRAW, p.Rect(3 * SQ_SIZE, 3.5 * SQ_SIZE, 2*SQ_SIZE, SQ_SIZE))
    if pawn_promotion:
        screen.blit(PAWNPROMOTION, p.Rect(2.5 * SQ_SIZE, 4 * SQ_SIZE, 4 * SQ_SIZE, SQ_SIZE))

def drawBoard(screen):
    """function to draw the screen"""
    colors = [p.Color("light grey"), p.Color([78,128,70])]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawSelected(screen,sqSelected):
    """fucntion to highlight the selected piece"""
    r = sqSelected[0]
    c = sqSelected[1]
    screen.blit(SELECTED, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    """function to draw all pieces from gamestate.board"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r,c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawLegalMoves(screen,legalSqs):
    """function to highlight the legal moves"""
    for i in legalSqs:
        r = i[0]
        c = i[1]
        screen.blit(LEGAL_MOVES, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    #bot.analyse_control(bot.get_influence_matrix(Engine.GameState()))
    main()
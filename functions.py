import copy
import os
import math
import time
import numpy as np
from moves_libary import *

class Gamestate():
    def __init__(self, p1_move1, p1_move2, p2_move1, p2_move2, stack, board, p_to_move):
        self.p1_move1 = p1_move1
        self.p1_move2 = p1_move2
        self.p2_move1 = p2_move1
        self.p2_move2 = p2_move2
        self.stack = stack
        self.board = board
        self.p_to_move = p_to_move


def init():
    default_board = np.array(
        [['bp', 'bp', 'bK', 'bp', 'bp'], ['  ', '  ', '  ', '  ', '  '], ['  ', '  ', '  ', '  ', '  '],
         ['  ', '  ', '  ', '  ', '  '], ['rp', 'rp', 'rK', 'rp', 'rp']])

    [move1, move2, move3, move4, move5] = get_moveset()
    p_to_move = math.ceil(2*np.random.rand(1,1))
    game_state = Gamestate(move1, move2, move4, move5, move3, default_board, p_to_move)
    return game_state




def check_for_win(board):
    bK_on_board = sum(sum(np.isin(board, 'bK')))
    rK_on_board = sum(sum(np.isin(board, 'rK')))
    red_win = board[0][2] == 'rK'
    blue_win = board[4][2] == 'bK'
    red_won = blue_won = 0

    if not (bK_on_board) or red_win:
        red_won = 1
    if not (rK_on_board) or blue_win:
        blue_won = 1

    return red_won, blue_won


def validate_move(game_state, move_input):
    # TODO keine eigenen Figuren schlagen!! und muss innerhalb vom board sein!

    # Zwischen p1 und p2 unterscheiden
    if game_state.p_to_move == 1:
        p = 1
        if move_input[0] == 1:
            compare = game_state.p1_move1.moves + np.array([int(move_input[1]), int(move_input[2])])
        if move_input[0] == 2:
            compare = game_state.p1_move2.moves + np.array([int(move_input[1]), int(move_input[2])])
    if game_state.p_to_move == 2:
        p = 2
        if move_input[0] == 1:
            compare = -game_state.p2_move1.moves + np.array([int(move_input[1]), int(move_input[2])])
        if move_input[0] == 2:
            compare = -game_state.p2_move2.moves + np.array([int(move_input[1]), int(move_input[2])])

    # Begrenzung des Feldes
    if 0 > int(move_input[3]) or int(move_input[3]) > 4 or 0 > int(move_input[4]) or int(move_input[4]) > 4:
        return False

    # Check ob eigene Figur auf Feld
    if not 'r' in game_state.board[int(move_input[1])][int(move_input[2])] and p == 1:
        return False
    elif not 'b' in game_state.board[int(move_input[1])][int(move_input[2])] and p == 2:
        return False

    # Check ob Feld durch eigene Figur belegt
    if 'r' in game_state.board[int(move_input[3])][int(move_input[4])] and p == 1:
        return False
    elif 'b' in game_state.board[int(move_input[3])][int(move_input[4])] and p == 2:
        return False
    else:
        move_is_valid = contains_move([int(move_input[3]), int(move_input[4])], compare)
    return move_is_valid


def contains_move(input, compare):
    isin = False
    for x in compare:
        if input[0] == x[0] and input[1] == x[1]:
            isin = True
    return isin


def make_move(game_state, engine_input=False):
    # Player input or engine input?
    new_game_state = copy.deepcopy(game_state)
    if not engine_input:
        # Check for legal move
        while True:
            temp = input('Please enter your move [move no; startpoint, endpoint]: (e.g. 1 01 11)\n')
            # move_input als liste mit int
            move_input = [int(x) for x in temp.replace(' ', '')]
            if validate_move(new_game_state, move_input):
                break
            print('No legal move, please try again ...')
    else:
        move_input = engine_input

    # Change the moves for the next turn
    if new_game_state.p_to_move == 1:
        # Swap moves
        if move_input[0] == 1:
            temp = new_game_state.stack
            new_game_state.stack = new_game_state.p1_move1
            new_game_state.p1_move1 = temp
        if move_input[0] == 2:
            temp = new_game_state.stack
            new_game_state.stack = new_game_state.p1_move2
            new_game_state.p1_move2 = temp

    if new_game_state.p_to_move == 2:
        # Swap moves
        if move_input[0] == 1:
            temp = new_game_state.stack
            new_game_state.stack = new_game_state.p2_move1
            new_game_state.p2_move1 = temp
        if move_input[0] == 2:
            temp = new_game_state.stack
            new_game_state.stack = new_game_state.p2_move2
            new_game_state.p2_move2 = temp

    # Swap p_to move
    if new_game_state.p_to_move == 1:
        new_game_state.p_to_move = 2
    else:
        new_game_state.p_to_move = 1

    # Figur bewegen
    temp = new_game_state.board[int(move_input[1])][int(move_input[2])]
    new_game_state.board[int(move_input[1])][int(move_input[2])] = '  '
    new_game_state.board[int(move_input[3])][int(move_input[4])] = temp

    return new_game_state


def visualize(game_state):
    os.system('CLS')
    print('    0      1      2      3      4    ' '\n' ' +------+------+------+------+------+' '\n' '0| ',
          game_state.board[0][0], ' | ', game_state.board[0][1], ' | ', game_state.board[0][2], ' | ',
          game_state.board[0][3], ' | ', game_state.board[0][4],
          ' |' '\n' ' +------+------+------+------+------+' '\n' '1| ', game_state.board[1][0], ' | ',
          game_state.board[1][1], ' | ', game_state.board[1][2], ' | ', game_state.board[1][3], ' | ',
          game_state.board[1][4], ' |' '\n' ' +------+------+------+------+------+''\n' '2| ', game_state.board[2][0],
          ' | ', game_state.board[2][1], ' | ', game_state.board[2][2], ' | ', game_state.board[2][3], ' | ',
          game_state.board[2][4], ' |' '\n' ' +------+------+------+------+------+' '\n' '3| ', game_state.board[3][0],
          ' | ', game_state.board[3][1], ' | ', game_state.board[3][2], ' | ', game_state.board[3][3], ' | ',
          game_state.board[3][4], ' |' '\n' ' +------+------+------+------+------+' '\n' '4| ', game_state.board[4][0],
          ' | ', game_state.board[4][1], ' | ', game_state.board[4][2], ' | ', game_state.board[4][3], ' | ',
          game_state.board[4][4], ' |' '\n' ' +------+------+------+------+------+')
    create_move_grafic(game_state)


def create_move_grafic(game_state):
    empty_card = np.array(
        [[' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ']])
    empty_card[2][2] = 'o'
    move1 = empty_card.copy()
    move2 = empty_card.copy()
    stack = empty_card.copy()
    move1e = empty_card.copy()
    move2e = empty_card.copy()

    if game_state.p_to_move == 1:
        # move 1
        for x in game_state.p1_move1.moves:
            move1[2 + x[0]][2 + x[1]] = '■'
        # move 2
        for x in game_state.p1_move2.moves:
            move2[2 + x[0]][2 + x[1]] = '■'
        # stack
        for x in game_state.stack.moves:
            stack[2 + x[0]][2 + x[1]] = '■'
        # move 1 Gegner
        for x in game_state.p2_move1.moves:
            move1e[2 + -x[0]][2 + -x[1]] = '■'
        # move 2 Gegner
        for x in game_state.p2_move2.moves:
            move2e[2 + -x[0]][2 + -x[1]] = '■'
    else:
        # OBACHT! bei p2 müssen die moves invertiert werden (dank clever definition einfach alle einträge *-1)
        # move 1
        for x in game_state.p2_move1.moves:
            move1[2 + -x[0]][2 + -x[1]] = '■'
        # move 2
        for x in game_state.p2_move2.moves:
            move2[2 + -x[0]][2 + -x[1]] = '■'
        # stack
        for x in game_state.stack.moves:
            stack[2 + -x[0]][2 + -x[1]] = '■'
        # move 1
        for x in game_state.p1_move1.moves:
            move1e[2 + x[0]][2 + x[1]] = '■'
        # move 2
        for x in game_state.p1_move2.moves:
            move2e[2 + x[0]][2 + x[1]] = '■'

    # Print all moves
    if game_state.p_to_move == 1:
        color = 'red'
    else:
        color = 'blue'

    print()
    print('Player ', game_state.p_to_move, '(', color, ')', ' is on the move!')
    print('Your moves: ')
    print('Move 1: ')
    print(move1)
    print()
    print('Move 2:')
    print(move2)
    print()
    print('Move on Stack:')
    print(stack)
    print()
    print('Enemy moves: ')
    print(move1e)
    print()
    print(move2e)
    print()

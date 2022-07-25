import numpy as np
import random
from functions import *


class Node:

    def __init__(self, evaluation):
        self.key = evaluation
        self.child = []


# Utility function to create a new tree node
def newNode(key):
    temp = Node(key)
    return temp


def run_game_against_engine():
    game_state = init()
    red_won = blue_won = 0
    visualize(game_state)
    while red_won == 0 and blue_won == 0:
        if game_state.p_to_move == 1:
            game_state = make_move(game_state)
        elif game_state.p_to_move == 2:
            game_state = make_move(game_state, best_engine_move(game_state))
            time.sleep(2)
        visualize(game_state)
        print('Positionsbewertung', evaluate_position(game_state.board))
        [red_won, blue_won] = check_for_win(game_state.board)
    print('red won : ', red_won)
    print('blue won: ', blue_won)


def test_engine_again_engine(game_count):
    red_won_count = blue_won_count = 0
    for x in range(game_count):
        os.system('CLS')
        print('Game_count: ', x)
        red_won = blue_won = 0
        game_state = init()
        while red_won == 0 and blue_won == 0:
            if game_state.p_to_move == 1:
                game_state = make_move(game_state, best_engine_move(game_state))
            elif game_state.p_to_move == 2:
                game_state = make_move(game_state, best_engine_move(game_state))
            [red_won, blue_won] = check_for_win(game_state.board)
        red_won_count += red_won
        blue_won_count += blue_won
    print('red won : ', red_won_count)
    print('blue won: ', blue_won_count)


def evaluate_position(board):
    # Bewertungsschema: negativ ist besser für p2 (blau), positiv besser für p1(rot)
    # geht von -inf bis +inf (verloren), wenn eine figur mehr, dann +- 10

    # TODO "Angegriffene" meiden (Wie auch immer das gehen soll :D)
    # TODO Anreiz für König schaffen, auf das Siegfeld zu kommen

    evaluation = 0

    [red_win, blue_win] = check_for_win(board)
    if red_win:
        return math.inf
    if blue_win:
        return -math.inf

    # Figuren zählen
    for x in board:
        for y in x:
            if 'r' in y:
                evaluation += 10
            elif 'b' in y:
                evaluation -= 10

    # Zentrale Positionen von Figuren bevorzugen ?!
    heatmap = np.array([[0, 1, 2, 1, 0], [1, 2, 3, 2, 1], [2, 3, 4, 3, 2], [1, 2, 3, 2, 1], [0, 1, 2, 1, 0]])
    for i in range(5):
        for j in range(5):
            if 'r' in board[i][j]:
                evaluation += heatmap[i][j]
            if 'b' in board[i][j]:
                evaluation -= heatmap[i][j]

    # König für Nähe zum Siegfeld belohnen
    bK_heatmap = np.array(
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 10, 10, 10, 0], [0, 10, math.inf, 10, 0]])
    rK_heatmap = np.array(
        [[0, 10, math.inf, 10, 0], [0, 10, 10, 10, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    for a in range(5):
        for b in range(5):
            if 'rK' in board[a][b]:
                evaluation += rK_heatmap[a][b]
            if 'bK' in board[a][b]:
                evaluation -= bK_heatmap[a][b]

    return evaluation


def get_all_possible_moves(game_state):
    list_of_possible_moves = []
    pieces = get_figure_position(game_state.board, game_state.p_to_move)
    if len(pieces) == 0:
        return []
    # p1 to move:
    if game_state.p_to_move == 1:
        for piece in pieces:
            # move 1
            for move in game_state.p1_move1.moves:
                # get move input string
                move_input = [1, int(piece[0]), int(piece[1]), int(piece[0]) + move[0], int(piece[1]) + move[1]]
                if validate_move(game_state, move_input):
                    list_of_possible_moves.append(move_input)
            # move 2
            for move2 in game_state.p1_move2.moves:
                # get move input string
                move_input2 = [2, int(piece[0]), int(piece[1]), int(piece[0]) + move2[0], int(piece[1]) + move2[1]]
                if validate_move(game_state, move_input2):
                    list_of_possible_moves.append(move_input2)
    elif game_state.p_to_move == 2:
        for piece in pieces:
            # Vorsicht, man muss moves für p2 invertrieren !!!
            # move 1
            for move in game_state.p2_move1.moves:
                # get move input string
                move_input = [1, int(piece[0]), int(piece[1]), int(piece[0]) - move[0], int(piece[1]) - move[1]]
                if validate_move(game_state, move_input):
                    list_of_possible_moves.append(move_input)
            # move 2
            for move2 in game_state.p2_move2.moves:
                # get move input string
                move_input2 = [2, int(piece[0]), int(piece[1]), int(piece[0]) - move2[0], int(piece[1]) - move2[1]]
                if validate_move(game_state, move_input2):
                    list_of_possible_moves.append(move_input2)
    return list_of_possible_moves


def best_engine_move(game_state):
    list_of_moves_lvl1 = get_all_possible_moves(game_state)
    list_of_gamestates_lvl1 = list()
    # root = AnyNode(id='root', previous_move=[], game_state=game_state)
    for move in list_of_moves_lvl1:
        list_of_gamestates_lvl1.append(make_move(game_state, move))
    # attach ojects to tree
    # TODO

    # lvl 2 errechenen und beste bewertung (für p1 bestimmen)
    evluation_of_lvl1 = list()
    for obj in list_of_gamestates_lvl1:
        list_of_moves_lvl2 = get_all_possible_moves(obj)
        list_of_gamestates_lvl2 = list()
        evluation_of_lvl2 = list()
        for move in list_of_moves_lvl2:
            list_of_gamestates_lvl2.append(make_move(obj, move))
        for obj2 in list_of_gamestates_lvl2:
            evluation_of_lvl2.append(evaluate_position(obj2.board))
        if game_state.p_to_move == 1 and len(
                evluation_of_lvl2):  # wenn p1 dran, dann min für best möglichen blauen move | Falls kein move möglich, ignorieren TODO Fix this! Im spiel muss man trotzdem einen move tauschen
            evluation_of_lvl1.append(min(evluation_of_lvl2))
        elif game_state.p_to_move == 2 and len(
                evluation_of_lvl2):  # wenn p2 dran, dann max für best möglichen roten move
            evluation_of_lvl1.append(max(evluation_of_lvl2))

    # besten move zurückgeben (random bei gleicher Bewertung)
    if game_state.p_to_move == 1:  # p1 ist dran -> max suchen
        temp = -math.inf
        max_list = []
        for i in range(0, len(evluation_of_lvl1) - 1):
            if evluation_of_lvl1[i] > temp:
                temp = evluation_of_lvl1[i]
                max_list = [i]
            elif evluation_of_lvl1[i] == temp:
                max_list.append(i)
        return list_of_moves_lvl1[max_list[random.randint(0, len(max_list) - 1)]]
    else:  # p1 ist dran -> min suchen
        temp = math.inf
        max_list = []
        for i in range(0, len(evluation_of_lvl1) - 1):
            if evluation_of_lvl1[i] < temp:
                temp = evluation_of_lvl1[i]
                max_list = [i]
            elif evluation_of_lvl1[i] == temp:
                max_list.append(i)
        return list_of_moves_lvl1[max_list[random.randint(0, len(max_list) - 1)]]


def get_figure_position(board, player_no):
    position_list = []
    for i in range(5):
        for j in range(5):
            if 'r' in board[i][j] and player_no == 1:
                position_list.append(str(''.join([str(i), str(j)])))
            elif 'b' in board[i][j] and player_no == 2:
                position_list.append(str(''.join([str(i), str(j)])))

    return position_list

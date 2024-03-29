import numpy as np
import random
from tree_class import *
from functions import *



def run_game_against_engine():
    game_state = init()
    red_won = blue_won = 0
    visualize(game_state)
    while red_won == 0 and blue_won == 0:
        if game_state.p_to_move == 1:
            game_state = make_move(game_state)
        elif game_state.p_to_move == 2:
            game_state = make_move(game_state, best_engine_move_tree(game_state))
            time.sleep(2)
        visualize(game_state)
        print('Positionsbewertung', evaluate_position(game_state.board))
        [red_won, blue_won] = check_for_win(game_state.board)
    print('red won : ', red_won)
    print('blue won: ', blue_won)


def test_engine_again_engine(game_count):
    red_won_count = blue_won_count = 0
    for x in range(game_count):
        print('Game_count: ', x)
        red_won = blue_won = 0
        game_state = init()
        while red_won == 0 and blue_won == 0:
            if game_state.p_to_move == 1:
                game_state = make_move(game_state, best_engine_move_tree(game_state))
            elif game_state.p_to_move == 2:
                game_state = make_move(game_state, best_engine_move_tree(game_state))
            [red_won, blue_won] = check_for_win(game_state.board)
        red_won_count += red_won
        blue_won_count += blue_won
    print('red won : ', red_won_count)
    print('blue won: ', blue_won_count)


def evaluate_position(board):
    # Bewertungsschema: negativ ist besser für p2 (blau), positiv besser für p1(rot)
    # geht von -inf bis +inf (verloren), wenn eine figur mehr, dann +- 10

    # TODO "Angegriffene" Felder meiden (Wie auch immer das gehen soll :D)
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
                # get move input string [move_no, start_x, start_y,end_x,end_y]
                move_input = [1, int(piece[0]), int(piece[1]), int(piece[0]) + move[0], int(piece[1]) + move[1]]
                if validate_move(game_state, move_input):
                    list_of_possible_moves.append(move_input)
            # move 2
            for move2 in game_state.p1_move2.moves:
                # get move input string
                move_input2 = [2, int(piece[0]), int(piece[1]), int(piece[0]) + move2[0], int(piece[1]) + move2[1]]
                if validate_move(game_state, move_input2):
                    list_of_possible_moves.append(move_input2)
    # p2 to move
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


def add_depth_2_to_node(game_state, input_node):
    list_of_moves_lvl1 = get_all_possible_moves(game_state)
    for move in list_of_moves_lvl1:
        # attach ojects to tree
        input_node.child.append(newNode(0, make_move(input_node.gamestate, move)))
    # lvl 2 errechenen und beste bewertung
    for i in range(len(input_node.child) - 1):
        list_of_moves_lvl2 = get_all_possible_moves(input_node.child[i].gamestate)
        # lvl 2 alle nodes erstellen
        for move in list_of_moves_lvl2:
            input_node.child[i].child.append(newNode(0, make_move(input_node.child[i].gamestate, move)))
        # alle nodes in lvl 2 bewerten
        for j in range(len(input_node.child[i].child) - 1):
            input_node.child[i].child[j].evaluation = evaluate_position(input_node.child[i].child[j].gamestate.board)


def best_engine_move_tree(game_state):
    list_of_moves_lvl1 = get_all_possible_moves(game_state)
    root = Node(0, game_state)
    add_depth_2_to_node(game_state, root)

    # ToDo: Richtige Suchalgorithmen für Bäume anwenden und nicht einfach alles durchiterieren

    # Hardcoded such nach bestem Zug
    #Beste Bewertung aus alle children (Tiefe 2) als Bewertung für eigene Moves eintragen (children tiefe 1) -> Bester Move des gegners wird als Bewertung eingetragen


    for i in range(0, len(root.child) - 1):
        root.child[i].evaluation = get_node_evalation(game_state, root.child[i])


    # besten move zurückgeben (random bei gleicher Bewertung)
    if game_state.p_to_move == 1:  # p1 ist dran -> max suchen
        temp = -math.inf
        max_list = [0]  # falls alle einträge -inf sind, einfach random einen wählen
        for i in range(0, len(root.child) - 1): #erste Ebene iteration
            if root.child[i].evaluation > temp:
                temp = root.child[i].evaluation
                max_list = [i]
            elif root.child[i].evaluation == temp:
                max_list.append(i)
        return list_of_moves_lvl1[max_list[(random.randint(1, len(max_list)) - 1)]]
    else:  # p2 ist dran -> min suchen
        temp = math.inf
        max_list = [0]  # falls alle einträge -inf sind, einfach den ersten nehmen
        for i in range(0, len(root.child) - 1): #erste Ebene iteration
                if root.child[i].evaluation < temp:
                    temp = root.child[i].evaluation
                    max_list = [i]
                elif root.child[i].evaluation == temp:
                    max_list.append(i)
        return list_of_moves_lvl1[max_list[(random.randint(1, len(max_list)) - 1)]]

# Methode um einer Node die beste (größte oder kleinste) Bewertung all seiner children zuzuordnen
# vorsicht, hier muss muss der beste Move für den gegner gefunden werden
def get_node_evalation(game_state, node):
    if game_state.p_to_move == 1:  # p2 hat gezogen -> min suchen
        evaluation = math.inf
        for i in range(0, len(node.child) - 1):
            if node.child[i].evaluation < evaluation:
                evaluation = node.child[i].evaluation
    else:  # p1 hat gezogen -> max suchen
        evaluation = -math.inf
        for i in range(0, len(node.child) - 1):  # erste Ebene iteration
            if node.child[i].evaluation > evaluation:
                evaluation = node.child[i].evaluation
    return evaluation


def get_figure_position(board, player_no):
    position_list = []
    for i in range(5):
        for j in range(5):
            if 'r' in board[i][j] and player_no == 1:
                position_list.append(str(''.join([str(i), str(j)])))
            elif 'b' in board[i][j] and player_no == 2:
                position_list.append(str(''.join([str(i), str(j)])))

    return position_list

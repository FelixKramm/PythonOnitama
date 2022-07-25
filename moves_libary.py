# Hier werden alle möglichen Zugkarten gespeichert und 5 zufällige ausgesucht
import random

import numpy as np


class Move:
    def __init__(self, name, moves):
        self.name = name
        self.moves = moves


def get_moveset():
    # alle moves definieren
    moveset = list()
    moveset.append(Move('Wildschwein', np.array([[0, -1], [-1, 0], [0, 1]])))
    moveset.append(Move('Gans', np.array([[-1, -1], [0, -1], [0, 1], [1, 1]])))
    moveset.append(Move('Kobra', np.array([[0, -1], [-1, 1], [1, 1]])))
    moveset.append(Move('Ochse', np.array([[-1, 0], [1, 0], [0, 1]])))
    moveset.append(Move('Aal', np.array([[-1, -1], [1, -1], [0, 1]])))
    moveset.append(Move('Affe', np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]])))
    moveset.append(Move('Pferd', np.array([[-1, 0], [0, -1], [1, 0]])))
    moveset.append(Move('Gottesanbeterin', np.array([[-1, 1], [-1, -1], [1, 0]])))
    moveset.append(Move('Frosch', np.array([[0, -2], [-1, -1], [1, 1]])))
    moveset.append(Move('Hahn', np.array([[1, -1], [0, -1], [0, 1], [-1, 1]])))
    moveset.append(Move('Hase', np.array([[1, -1], [-1, 1], [0, 2]])))
    moveset.append(Move('Drache', np.array([[-1, -2], [1, -1], [1, 1], [-1, 2]])))
    moveset.append(Move('Kranich', np.array([[-1, 0], [1, -1], [1, 1]])))
    moveset.append(Move('Tiger', np.array([[-2, 0], [1, 0]])))
    moveset.append(Move('Krabbe', np.array([[0, -2], [0, 2], [-1, 0]])))
    moveset.append(Move('Elefant', np.array([[-1, 1], [-1, -1], [0, 1], [0, -1]])))

    return random.sample(moveset, 5)

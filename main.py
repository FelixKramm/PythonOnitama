import math
from functions import *
from engine import *
import time


if __name__ == '__main__':
    if input('human vs cpu[1] or cpu vs cpu[2]?') == '1':
        run_game_against_engine()
    else:
        st = time.time()
        test_engine_again_engine(10)
        et = time.time()
        print('Execution time: ', round(et-st,2))

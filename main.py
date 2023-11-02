import math
from functions import *
from engine import *
from GUI import *
import time


if __name__ == '__main__':
    #gui()
    if input('human vs cpu[1] or cpu vs cpu[2]? \n') == '1':
        run_game_against_engine()
    else:
        st = time.time()
        test_engine_again_engine(1000)
        et = time.time()
        print('Execution time: ', round(et-st,2))

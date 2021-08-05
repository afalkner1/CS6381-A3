import sys
from random import randrange

import time
import random

class topic():

    def __init__(self, tp):
        self.history = 3
        self.window = ["0", "0", "0"]
        self.count = 0
        self.index = ""


    def run(self):
        rec_time = time.time()
        time1 = 1626388858.77716
        dif = rec_time - time1
        print(dif)


if __name__ == "__main__":

    t = topic(8)
    t.run()



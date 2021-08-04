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
        while True:
            self.count = 0;
            while self.count < self.history:
                blah = random.randrange(0, 50)
                print(f"blah: {blah}")
                msg = f'{blah}'
                self.window[self.count] = msg
                self.index = "["
                for w in self.window:
                    self.index = self.index + " " + w
                self.index = self.index + " ]"
                print(self.index)
                self.count = self.count + 1
                time.sleep(1)


if __name__ == "__main__":

    t = topic(8)
    t.run()



import time

class Timer:
    def __init__ (self):
        self.times = [0, 0, 0]

    def tick (self):
        self.t0 = time.clock ()

    def tock (self, i):
        self.times [i] += time.clock () - self.t0

    def __str__ (self):
        s = sum (self.times)
        r = ""
        r += "Movement Time: " + str (self.times [0]) + "\t%" + str (100 * self.times [0] / s)
        r += "\nCamera Time:   " + str (self.times [1]) + "\t%" + str (100 * self.times [1] / s)
        r += "\nRender Time:   " + str (self.times [2]) + "\t%" + str (100 * self.times [2] / s)
        return r + "\n"

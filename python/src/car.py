import numpy as np

class Car:
    def __init__(self):
        self.steer = 0
        self.throttle = 0
        
        self.steer_p_gain = 2
        
    def __del__(self):
        pass
    
#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Kinematic Bicycle Model
author Atsushi Sakai (https://github.com/AtsushiSakai/PyAdvancedControl/blob/master/steer_vehicle_model/kinematic_bicycle_model.py)
edited by Hirotaka Hosogaya
"""

import numpy as np

class KBM:
    def __init__(self, L, Lr, y=0.0, psi=0.0, v=0.0, beta=0.0):
        self.L = L
        self.Lr = Lr
        self.x = Lr
        self.y = y
        self.psi = psi
        self.v = v
        self.beta = beta


    def update(self, a, delta, dt):
        self.beta = np.arctan2(self.Lr / self.L * np.tan(delta), 1.0)
        self.x = self.x + self.v * np.cos(self.psi + self.beta) * dt
        self.y = self.y + self.v * np.sin(self.psi + self.beta) * dt
        self.psi = self.psi + self.v / self.Lr * np.sin(self.beta) * dt
        self.v = self.v + a * dt
        
class OriginalKBM:
    def __init__(self, L, Lr, y=0.0, psi=0.0, v=0.0):
        self.L = L
        self.Lr = Lr
        self.x = Lr
        self.y = y
        self.psi = psi
        self.v = v
        
    def update(self, a, delta, dt):
        beta = np.arctan2(self.Lr / self.L * np.tan(delta), 1.0)
        dx = self.v * np.cos(beta) * dt
        dy = self.v * np.sin(beta) * dt
        dv = a * dt
        dp = self.v/self.Lr * np.sin(beta) * dt
        
        return dx, dy, dp, dv
        
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    car = KBM(L = 2.9, Lr=1.5)
    # car = OriginalKBM(L = 2.9, Lr=1.5)
    x = []
    y = []
    v = []
    psi = []
    t = []
    a = 10.0 # 加速度
    delta = np.pi / 36 # 操舵角
    dt = 0.01
    for i in range(1000):
        t.append(dt * i)
        # dx, dy, dp, dv = car.update(a, delta)
        # car.x = car.x + (dx * np.cos(car.psi) - dy * np.sin(car.psi)) 
        # car.y = car.y + (dx * np.sin(car.psi) + dy * np.cos(car.psi)) 
        # car.psi = car.psi + dp 
        # car.v = car.v + dv 
        x.append(car.x)
        y.append(car.y)
        psi.append(car.psi)
        v.append(car.v)
        car.update(a, delta, dt)
        
    fig = plt.figure(figsize=(12, 6))
    fig_xy = fig.add_subplot(121)
    fig_vy = fig.add_subplot(122)
    
    fig_xy.plot(x, y, label = "x-y")
    fig_vy.plot(v, psi, label = "v-psi")
    
    plt.show()
    # fig.savefig("out_original.png")
    fig.savefig("out_kbm.png")
    
    
    
    
    
    
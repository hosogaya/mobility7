import numpy as np
import pigpio

class Motor:
    # コンストラクタ：インスタンス生成時に呼び出される
    def __init__(self, throttle_pin = 18, steer_pin = 17):
        self.THROTTLE_PIN = throttle_pin # 駆動力を入力するGPIOピン
        self.STEER_PIN = steer_pin # 操舵入力をするGPIOピン
        self.gpio = pigpio.pi() # モータの出力用
        self.THROTTLE_BIAS = 1500 # 駆動力の原点の位置
        self.STEER_BIAS = 1500 # 操舵の原点の位置
        self.MIN_PWM = 700
        self.MAX_PWM = 2300
        
    # デストラクタ
    # 破棄されるときに呼び出される
    # 操舵角と駆動力を０にする．
    def __del__(self):
        self.gpio.set_servo_pulsewidth(self.THROTTLE_PIN, self.THROTTLE_BIAS)
        self.gpio.set_servo_pulsewidth(self.STEER_PIN, self.STEER_BIAS)
    
    # 駆動力を入力 
    def Throttle(self, value):
        out = -int(value) + self.THROTTLE_BIAS
        if out < self.MIN_PWM: out = self.MIN_PWM
        elif out > self.MAX_PWM: out = self.MAX_PWM
        self.gpio.set_servo_pulsewidth(self.THROTTLE_PIN, out)
        
    # 操舵の入力
    def Steer(self, value):
        out = int(value) + self.STEER_BIAS
        if out < self.MIN_PWM: out = self.MIN_PWM
        elif out > self.MAX_PWM: out = self.MAX_PWM
        self.gpio.set_servo_pulsewidth(self.STEER_PIN, out)
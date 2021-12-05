from image_processing import *
from motor_driver import *
from car import *

import time
import signal

# 画像の色検出結果を出力するテスト関数
def Stream(cam):
    while cv2.waitKey(30) < 0:
        ret, frame = cam.getFrame()
        if ret == True:
            mask = cam.red_mask(frame)
            rects = cam.getRects(mask)
            for rect in rects:
                cv2.drawContours(frame, [rect], 0, (0, 0, 255), thickness=2)
                
            cv2.imshow("origin", frame)
            cv2.imshow("masked", mask)
    cv2.destroyAllWindows()
    
# ラインを検出しながらモータへの制御入力を行い走行する
def driving(car, cam, motor):
    car.throttle = 30
    while cv2.waitKey(30) < 0:
        start_time = time.perf_counter()
        ret, frame = cam.getFrame()
        if ret == True:
            mask = cam.white_mask(frame)
            rects = cam.getRects(mask)
            
            # 最大の短形状を抽出して制御入力を決める
            # 短形状がなかったらループを抜け出す
            if len(rects) > 0: 
                max_rect = max(rects, key = (lambda x: cv2.contourArea(x)))
                center = cam.getCenter(max_rect)
                car.steer = center[0] * car.steer_p_gain
            else: 
                motor.Steer(0)
                motor.Throttle(0)
                break
            
            #　モータに入力
            motor.Steer(car.steer)
            motor.Throttle(car.throttle)
            end_time = time.perf_counter() 
            
            # 実行にかかっている時間をミリ秒で表示
            print("Execution time : %d" %((end_time - start_time) * 1000))
            # 画像表示
            for rect in rects:
                cv2.drawContours(frame, [rect], 0, (0, 0, 255), thickness=2)
            cv2.imshow("origin", frame)
            cv2.imshow("binary", mask)
            
    cv2.destroyAllWindows()

# ここがプログラムのスタート地点
if __name__ == "__main__":
    cam = Camera()
    motor = Motor()
    car = Car()
    # Stream(cam) # カメラが見ている画像を表示
    driving(car, cam, motor)
    del cam, motor, car
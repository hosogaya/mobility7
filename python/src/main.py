from cv2 import TermCriteria_COUNT
from image_processing import *
from motor_driver import *
from car import *

import time
import threading
import signal

stop_flag = False

# 画像の色検出結果を出力するテスト関数
def Stream(cam):
    while cv2.waitKey(30) < 0:
        ret, frame = cam.getFrame()
        if ret == True:
            mask = cam.white_mask(frame)
            mask = cam.geometryMask(mask)
            rects = cam.getRects(mask)
            for rect in rects:
                cv2.drawContours(frame, [rect], 0, (0, 0, 255), thickness=2)
                
            cv2.imshow("origin", frame)
            cv2.imshow("masked", mask)
    cv2.destroyAllWindows()
    
# カメラ画像を表示するときに停止信号を受信するための関数
def stop():
    global stop_flag
    while stop_flag == False:
        str = input()
        if str == 'stop':
            stop_flag = True
        
# カメラ画像を読み込み１ステップ分の制御を実施する
def control(car, cam, motor, camera_test):
    car.throttle = 30
    start_time = time.perf_counter()
    ret, frame = cam.getFrame()
    if ret == True:
        mask = cam.geometryMask(frame)
        white_mask = cam.white_mask(mask)
        w_rects = cam.getRects(white_mask) # 白色画像認識
        # 最大の短形状を抽出して制御入力を決める
        # 短形状がなかったらループを抜け出す（止まる）
        if len(w_rects) > 0: 
            max_rect = max(w_rects, key = (lambda x: cv2.contourArea(x)))
            center = cam.getCenter(max_rect, white_mask)
            car.steer = center[0] * car.steer_p_gain
        else: 
            motor.Steer(0)
            motor.Throttle(0)
            return None
        
        # 停止のため
        blue_mask = cam.blue_mask(mask)
        b_rects = cam.getRects(blue_mask) # 青色の輪郭抽出
        threshold = 500
        if len(b_rects):
            max_Brect = b_rects
            flag = False
            for rect in b_rects:
                area = cv2.contourArea(rect)
                if area > threshold:
                    max_Brect = rect
                    threshold = area
                    flag = True
                    
            if car.detect == True :
                if flag == True: # 一時停止を見つけた
                    motor.Throttle(-800) # 一回大きな入力を与える
                    time.sleep(0.1)
                    motor.Throttle(0) # 
                    motor.Steer(0)
                    time.sleep(3)
                    car.detect = False
                else: # 一時停止を抜けている途中
                    car.detect == True
            
            elif car.detect == False:
                if flag == False: # 一時停止を抜けた
                    car.detect = True
        
        
        #　モータに入力
        motor.Steer(car.steer)
        motor.Throttle(car.throttle)
        # print(car.steer)
        # print(threshold)\
        end_time = time.perf_counter() 
        
        # 画像表示
        if camera_test: # 表示にも時間がかかるため，テスト走行時のみ表示する
            if len(w_rects) > 0:
                for rect in w_rects:
                    cv2.drawContours(frame, [rect], 0, (0, 0, 255), thickness=2)
            cv2.imshow("origin", frame)
            cv2.imshow("binary", white_mask)
            
        # 実行にかかっている時間をミリ秒で表示
        print("Execution time : %d" %((end_time - start_time) * 1000))


# ラインを検出しながらモータへの制御入力を行い走行する
# カメラ画像を表示しない場合にはcv2.waitKey()が働かない
# cv2.imshowがおそらくthreadingに対応していない
# そのためカメラ画像表示のON/OFFに合わせて処理を変えている
def driving(car, cam, motor, camera_test = False):
    if camera_test:
        while cv2.waitKey(1) < 0:
            control(car, cam, motor, camera_test)
            print(car.steer)
        cv2.destroyAllWindows()
        
    else:
        global stop_flag
        def move():
            while stop_flag == False:
                control(car, cam, motor, camera_test)
                
        thread1 = threading.Thread(target=move)
        thread2 = threading.Thread(target=stop)
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        

# ここがプログラムのスタート地点
if __name__ == "__main__":
    cam = Camera()
    motor = Motor()
    car = Car()
    # Stream(cam) # カメラが見ている画像を表示
    driving(car, cam, motor, camera_test = True) # カメラ画像を表示するときはcamera_test = True
    del cam, motor, car
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
            mask = cam.red_mask(frame)
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
        mask = cam.white_mask(frame)
        rects = cam.getRects(mask)
        
        # 最大の短形状を抽出して制御入力を決める
        # 短形状がなかったらループを抜け出す（止まる）
        if len(rects) > 0: 
            max_rect = max(rects, key = (lambda x: cv2.contourArea(x)))
            center = cam.getCenter(max_rect)
            car.steer = center[0] * car.steer_p_gain
        else: 
            motor.Steer(0)
            motor.Throttle(0)
            return None
        
        #　モータに入力
        motor.Steer(car.steer)
        motor.Throttle(car.throttle)
        end_time = time.perf_counter() 
        
        # 画像表示
        if camera_test: # 表示にも時間がかかるため，テスト走行時のみ表示する
            for rect in rects:
                cv2.drawContours(frame, [rect], 0, (0, 0, 255), thickness=2)
            cv2.imshow("origin", frame)
            cv2.imshow("binary", mask)
            
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
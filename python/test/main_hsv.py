# https://qiita.com/hsgucci/items/e9a65d4fa3d279e4219e 参照
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time         # time.sleepを使いたいので
import cv2          # OpenCVを使うため
import numpy as np

# メイン関数
def main():
    # Telloクラスを使って，droneというインスタンス(実体)を作る
    cap = cv2.VideoCapture(0)
    current_time = time.time()  # 現在時刻の保存変数
    pre_time = current_time     # 5秒ごとの'command'送信のための時刻変数

    time.sleep(0.5)     # 通信が安定するまでちょっと待つ

    # トラックバーを作るため，まず最初にウィンドウを生成
    cv2.namedWindow("OpenCV Window")

    # トラックバーのコールバック関数は何もしない空の関数
    def nothing(x):
        pass
    
    print("before Track bars")
    # トラックバーの生成
    cv2.createTrackbar("H_min", "OpenCV Window", 0, 179, nothing)       # Hueの最大値は179
    cv2.createTrackbar("H_max", "OpenCV Window", 128, 179, nothing)
    cv2.createTrackbar("S_min", "OpenCV Window", 128, 255, nothing)
    cv2.createTrackbar("S_max", "OpenCV Window", 255, 255, nothing)
    cv2.createTrackbar("V_min", "OpenCV Window", 128, 255, nothing)
    cv2.createTrackbar("V_max", "OpenCV Window", 255, 255, nothing)

    print("start loop")
    #Ctrl+cが押されるまでループ
    try:
        while cv2.waitKey(20) < 0:
            # (A)画像取得
            ret, frame = cap.read()    # 映像を1フレーム取得
            if ret == False:    # 中身がおかしかったら無視
                print("faild to read frame")
                continue 

            print("success to read frame")
            # (B)ここから画像処理
            frame = cv2.rotate(frame, cv2.ROTATE_180) # 180度回転
            # image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)      # OpenCV用のカラー並びに変換する
            image = frame
            bgr_image = cv2.resize(image, dsize=(320,240) ) # 画像サイズを半分に変更

            hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)  # BGR画像 -> HSV画像

            # トラックバーの値を取る
            h_min = cv2.getTrackbarPos("H_min", "OpenCV Window")
            h_max = cv2.getTrackbarPos("H_max", "OpenCV Window")
            s_min = cv2.getTrackbarPos("S_min", "OpenCV Window")
            s_max = cv2.getTrackbarPos("S_max", "OpenCV Window")
            v_min = cv2.getTrackbarPos("V_min", "OpenCV Window")
            v_max = cv2.getTrackbarPos("V_max", "OpenCV Window")

            hsv_image = cv2.GaussianBlur(hsv_image, ksize=(9,9), sigmaX = 3.0)

            # inRange関数で範囲指定２値化 -> マスク画像として使う
            mask_image = cv2.inRange(hsv_image, (h_min, s_min, v_min), (h_max, s_max, v_max)) # HSV画像なのでタプルもHSV並び

            # bitwise_andで元画像にマスクをかける -> マスクされた部分の色だけ残る
            result_image = cv2.bitwise_and(hsv_image, hsv_image, mask=mask_image)
            
            # 輪郭抽出
            contours, _ = cv2.findContours(mask_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            rects = contours
            # rects = [np.int0(cv2.boxPoints(cv2.minAreaRect(cv2.convexHull(contour)))) for contour in contours]
            if len(rects) > 0:
                for rect in rects:
                    cv2.drawContours(bgr_image, [rect], 0, (0, 0, 255), thickness=2)
            # (X)ウィンドウに表示
            cv2.imshow('OpenCV Window', result_image)   # ウィンドウに表示するイメージを変えれば色々表示できる
            cv2.imshow('original image', bgr_image)

    except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
        print( "SIGINTを検知" )
        cap.release()
        cv2.destroyAllWindows()


# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":      # importされると"__main__"は入らないので，実行かimportかを判断できる．
    main()    # メイン関数を実行

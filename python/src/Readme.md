# プログラムの解説

## 構成
基本的に実行するのは`main.py`となります．その他のファイルはmain.pyから呼び出す関数を種別ごとに分けて定義しているものです（その予定です）．

### image_processing.py
カメラとの接続や設定と画像処理を行う`Camera`クラスを定義している． 


```python
# モジュールのインポート
from image_processing import *

# 引数は左から，カメラまでのパス，180度回転するかどうか，横幅，縦幅
cam = Camera(camera_path = 0, rotate = True, width = 320, height = 240)
while cv2.waitKey(0) < 0: # キーボード入力でbreak
    ret, frame = cam.getFrame() # 1フレームの画像を取得
    if ret == True: # 取得成功
        mask = cam.red_mask(frame) # 赤色検出
        rects = cam.getRects(mask) # 短形状抽出
        for rect in rects: # すべての短形状を描画
            cv2.drawContours(frame, [rect], 0, (0, 0, 255), thickness=2)
            
        cv2.imshow("origin", frame) # 元の画像の出力
        cv2.imshow("masked", mask) # 赤色検出をした2値化画像を出力
cv2.destroyAllWindows() # ウインドウを破棄
```
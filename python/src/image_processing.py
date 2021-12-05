import cv2
import numpy as np 


# カメラとの接続，設定と画像処理についての関数をまとめたもの
class Camera:
    # self : クラスない関数では常にこれを最初に引数として設定します
    # camera_path : 接続するカメラまでのパス
    # rotate : 180度かいてんさせるか（True:回転する，False:しない）
    def __init__(self, camera_path = 0, rotate = True, width = 320, height = 240):
        self.width = width
        self.height = height
        self.rotate = rotate
        self.cap = cv2.VideoCapture(camera_path)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
    def __del__(self):
        self.cap.release()

    # 1フレーム分の画像を取得
    # ret : 画像が取得できたか（True:成功，False:失敗)
    # frame : 画像データ
    def getFrame(self):
        ret, frame = self.cap.read()
        if self.rotate & ret:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        return ret, frame

    def red_mask(self, src):
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV_FULL)
        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]
        dist =  np.zeros(h.shape, dtype=np.uint8)
        dist[(h < 10) & (s > 128)] = 255
        dist[(h > 200) & (s > 128)] = 255
        return dist
    
    def white_mask(self, src):
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV_FULL)
        hsv = cv2.GaussianBlur(hsv, ksize=(9,9), sigmaX = 3.0)
        h, s, v = cv2.split(hsv)
        dist =  np.zeros(h.shape, dtype=np.uint8)
        dist[(h >60) & (s > 2) & (v > 70)] = 255 # white
        dist[(h < 130) & (s < 10) & (v < 160)] = 255
        return dist
    
    # 画像中から一色で塗りつぶされている短形状を探索して，それらの頂点の座標を獲得する．
    def getRects(self, src):
        contours, _ = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = [np.int0(cv2.boxPoints(cv2.minAreaRect(cv2.convexHull(contour)))) for contour in contours]
        return rects
    
    # 与えられた四角形の中心位置を画像の位置を返す
    # 絶対座標（左上を原点とした座標）が欲しい場合はabs = Trueに
    def getCenter(self, rect, abs = False):
        center = sum(rect)
        center[0] = center[0] - self.width/2
        center[1] = center[1] - self.height/2
        return center
    
    def MeanFilter(self, frame):
        kernel = np.array([[1/9, 1/9, 1/9],
                           [1/9, 1/9, 1/9],
                           [1/9, 1/9, 1/9]])
        dist = cv2.filter2D(frame, -1, kernel)
        return dist
    
    def EdgeEnhancement(self, frame):
        kernel = np.array([[-1,-1,-1],
                           [-1, 9,-1],
                           [-1,-1,-1]])
        dist = cv2.filter2D(frame, -1, kernel)
        return dist
    
import cv2
import numpy as np 

class Camera:
    # camera_path : path of camera
    def __init__(self, camera_path = 0):
        self.width = 320
        self.height = 240
        self.cap = cv2.VideoCapture(camera_path)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
    def __del__(self):
        self.cap.release()

    # 1フレーム分の画像を取得
    # ret : 画像が取得できたか（True:成功，False:失敗)
    # frame : 画像データ
    def getFrame(self):
        self.ret, self.frame = self.cap.read()
        return self.ret, self.frame

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
        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]
        dist =  np.zeros(h.shape, dtype=np.uint8)
        dist[(h < 50) & (s > 2) & (v > 70)] = 255 # white
        dist[(h < 100) & (s < 10) & (v < 120)] = 255
        return dist
    
    # 画像中から一色で塗りつぶされている短形状を探索して，それらの頂点の座標を獲得する．
    def getRects(self, src):
        contours, _ = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = [np.int0(cv2.boxPoints(cv2.minAreaRect(cv2.convexHull(contour)))) for contour in contours]
        return rects
    
    def getCenter(self, rect):
        center = rect.sum() / 4
        center[0] = center[0] - self.width/2
        center[1] = center[1] - self.height/2
    
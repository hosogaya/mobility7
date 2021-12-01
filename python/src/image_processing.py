import cv2
import numpy as np 

class Camera:
    # camera_path : path of camera
    def __init__(self, camera_path = 0):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        
    def __del__(self):
        self.cap.release()

    def getImage(self):
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
    
import cv2
import numpy as np
from ipywidgets import widgets, fixed


def inRange(img, c1, c2, c3):
    """2値化処理を行い、結果を表示する。
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([c1[0], c2[0], c3[0]])
    upper = np.array([c1[1], c2[1], c3[1]])

    bin_img = cv2.inRange(hsv, lower, upper)
    cv2.imshow(bin_img)


# パラメータ lower, upper を設定するスライダー
names = ["H", "S", "V"]
parts = {}
for i, name in enumerate(names, 1):
    slider = widgets.SelectionRangeSlider(
        options=np.arange(256), index=(0, 255), description=name
    )
    slider.layout.width = "400px"
    parts[f"c{i}"] = slider

# 画像を読み込む。
cap = cv2.VideoCapture(0)
ret = False
while ret == False:
    ret, img = cap.read()
    # ウィジェットを表示する。
widgets.interactive(inRange, **parts, img=fixed(img))
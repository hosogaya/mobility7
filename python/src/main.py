from image_processing import *

# for test image processing
# cam : instance of Camera class
def Stream(cam):
    while cv2.waitKey(30) < 0:
        ret, frame = cam.getFrame()
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        if ret == True:
            mask = cam.red_mask(frame)
            rects = cam.getRects(mask)
            for rect in rects:
                cv2.drawContours(frame, [rect], 0, (0, 0, 255), thickness=2)
                
            cv2.imshow("origin", frame)
            cv2.imshow("masked", mask)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = Camera()
    Stream(cam)
    del cam
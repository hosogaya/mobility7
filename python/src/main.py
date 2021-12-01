from image_processing import *

if __name__ == "__main__":
    cam = Camera()
    ret, frame = cam.getImage()
    if ret == True:
        mask = cam.red_mask(frame)
        cv2.imshow("test", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cam.cap.release()
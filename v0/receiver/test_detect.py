from detect import Detector
import cv2

from utils import plot_one_box

video = 0


def main():
    print("test detect")

    detector=Detector()

    cap = cv2.VideoCapture(video)
    success, img0 = cap.read()

    while(success):
        success, img0 = cap.read()  #读取摄像头照片
        if success:
            ids=detector.identify(img0)   # 0,1
            print(ids)

            boxs=detector.get_boxs(img0)
            print(boxs)

            for box in boxs:
                plot_one_box(box,img0,(255,0,0),'test')   #bgr
            
            
            cv2.imshow('flag_win',img0) 
            

            # cv2.imshow('flag_win',img0)
        cv2.waitKey(500)



if __name__ == '__main__':
    main()


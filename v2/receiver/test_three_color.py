import re
import cv2
from CQRCode import Decoder
import numpy as np
import os


MODE=0



# def someblur(src, blursize = 5):
#     # dst = cv2.blur(src, (blursize, blursize))
#     dst = cv2.GaussianBlur(src, (blursize, blursize), 1)
#     return dst

# def desharpen(src):
#     blur = someblur(src, 5)
#     dst = cv2.addWeighted(src, 0.5, blur, 0.5, 0)
#     return dst

decoder=Decoder()


cv2.namedWindow('test',cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow('test_R',cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow('test_G',cv2.WINDOW_GUI_NORMAL)
#cv2.namedWindow('img_1',cv2.WINDOW_GUI_NORMAL)
#cv2.namedWindow('img_2',cv2.WINDOW_GUI_NORMAL)
cnt=0



if MODE==0:
    cap=cv2.VideoCapture(0)


    #cap.set(cv2.CAP_PROP_BRIGHTNESS,0.5)
    while(True):
        
        ret,frame=cap.read()
        

        # scale = 0.5  # whatever scale you want
        # frame_darker = (frame * scale).astype(np.uint8)


        img_R,img_G,img_B,data=decoder.CQRCode_decode(frame,qrcode_type=3,test=True)
        
        #dark_image = np.zeros(img_R.shape, dtype=img_R.dtype)

        #cv2.imshow('test_G',img_R)

        #img_R2=decoder.Light_adjust(img_R)
        #decoder.QRCode_decodeDisplay(img_G2,"test_G")

        cv2.imshow('test',frame)

        cv2.imshow('test_G',img_G)

        cv2.imshow('test_R',img_R)


        

        print(data)
        #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
        #cv2.imshow('test_R',img_R2)
        #
        #cv2.imshow('test',img)
        cv2.waitKey(500)

elif MODE==1:
    frame=cv2.imread('test3.jpg')
    img_R,img_G,data=decoder.CQRCode_decode(frame,test=True)
    cv2.imshow('test',frame)

    cv2.imshow('test_G',img_G)

    cv2.imshow('test_R',img_R)
    print(data)
    #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
    #cv2.imshow('test_R',img_R2)
    #
    #cv2.imshow('test',img)
    cv2.waitKey(0)

elif MODE==2:
    tests=os.listdir("tests")
    for img in tests:
        frame=cv2.imread("tests/"+img)
        img_R,img_G,img_B,data=decoder.CQRCode_decode(frame,qrcode_type=3,test=True)
        cv2.imshow('test',frame)

        cv2.imshow('test_G',img_G)

        cv2.imshow('test_R',img_R)
        print(data)

        if(data!=None):
            cnt+=1
        #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
        #cv2.imshow('test_R',img_R2)
        #
        #cv2.imshow('test',img)
        cv2.waitKey(5000)
        

    print(cnt)

elif MODE==3:
    tests=os.listdir("tests")
    for img in tests:
        frame=cv2.imread("tests/"+img)
        img_R,img_G,data=decoder.CQRCode_decode(frame,test=True)
        cv2.imshow('test',frame)

        cv2.imshow('test_G',img_G)

        cv2.imshow('test_R',img_R)
        print(data)

        if(data!=None):
            cnt+=1
        #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
        #cv2.imshow('test_R',img_R2)
        #
        #cv2.imshow('test',img)
        cv2.waitKey(5000)
        

    print(cnt)
# img[:,:,2]=np.maximum(img[:,:,0],img[:,:,2])

# #print(img[:,:,0])


# #img=desharpen(img)

# gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# gray=cv2.bilateralFilter(gray,  7, 300, 10)



# ret,img=cv2.threshold(gray,145, 255,cv2.THRESH_BINARY)




#print(img)

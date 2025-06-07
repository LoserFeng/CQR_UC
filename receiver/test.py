import re
import cv2
from CQRCode import Decoder,Encoder
import numpy as np
import os
import math

MODE=6



# def someblur(src, blursize = 5):
#     # dst = cv2.blur(src, (blursize, blursize))
#     dst = cv2.GaussianBlur(src, (blursize, blursize), 1)
#     return dst

# def desharpen(src):
#     blur = someblur(src, 5)
#     dst = cv2.addWeighted(src, 0.5, blur, 0.5, 0)
#     return dst

decoder=Decoder()

def nothing(x):
    pass

# cv2.create('Value of Gamma','demo',100,1000,nothing)#使用滑动条动态调节参数gamma

# cv2.namedWindow('orig',cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow('test',cv2.WINDOW_GUI_NORMAL)
# cv2.namedWindow('test2',cv2.WINDOW_GUI_NORMAL)
# cv2.namedWindow('test_R',cv2.WINDOW_GUI_NORMAL)
# cv2.namedWindow('test_G',cv2.WINDOW_GUI_NORMAL)
# cv2.namedWindow('test_B',cv2.WINDOW_GUI_NORMAL)
#cv2.namedWindow('img_1',cv2.WINDOW_GUI_NORMAL)
#cv2.namedWindow('img_2',cv2.WINDOW_GUI_NORMAL)
cnt=0



# if MODE==0:
#     cap=cv2.VideoCapture(0)

#     # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1.0) # 再关闭自动曝光
#     # cap.set(cv2.CAP_PROP_EXPOSURE, exposure) # 最后设置曝光参数


#     #cap.set(cv2.CAP_PROP_BRIGHTNESS,0.5)
#     while(True):
        
#         ret,frame=cap.read()
        

#         # scale = 0.5  # whatever scale you want
#         # frame_darker = (frame * scale).astype(np.uint8)

#         # adjust_frame=decoder.gamma_trans(frame)

#         img_R,img_G,data=decoder.CQRCode_decode(frame,True,adjust_light=False)
        
#         #dark_image = np.zeros(img_R.shape, dtype=img_R.dtype)

#         #cv2.imshow('test_G',img_R)

#         #img_R2=decoder.Light_adjust(img_R)
#         #decoder.QRCode_decodeDisplay(img_G2,"test_G")

#         cv2.imshow('test',frame)

#         # cv2.imshow('test_adjust',adjust_frame)

#         cv2.imshow('test_G',img_G)

#         cv2.imshow('test_R',img_R)


        

#         print(data)
#         #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
#         #cv2.imshow('test_R',img_R2)
#         #
#         #cv2.imshow('test',img)
#         cv2.waitKey(500)

# elif MODE==1:
#     frame=cv2.imread('test3.jpg')
#     img_R,img_G,data=decoder.CQRCode_decode(frame,test=True,adjust_light=True)
#     cv2.imshow('test',frame)

#     cv2.imshow('test_G',img_G)

#     cv2.imshow('test_R',img_R)
#     print(data)
#     #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
#     #cv2.imshow('test_R',img_R2)
#     #
#     #cv2.imshow('test',img)
#     cv2.waitKey(0)



# elif MODE==2:
#     tests=os.listdir("tests")

#     total =len(tests)
#     for img in tests:
#         frame=cv2.imread("tests/"+img)
#         img_R,img_G,R_data,G_data=decoder.CQRCode_decode_test2(frame)
#        # cv2.imshow('test',frame)

#        # cv2.imshow('test_G',img_G)

#        # cv2.imshow('test_R',img_R)
        

#         if(R_data!=None and G_data!=None):
#             cnt+=1

#         if(R_data==None and G_data==None):
#             total-=1
#         #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
#         #cv2.imshow('test_R',img_R2)
#         #
#         #cv2.imshow('test',img)
#         #cv2.waitKey(1000)
        

#     print("total:",total)
#     print("success:",cnt)


# elif MODE==3:
#     tests=os.listdir("tests")
#     total=len(tests)
#     for img in tests:
#         frame=cv2.imread("tests/"+img)
#         img_R,img_G,img_B,R_data,G_data,B_data,data=decoder.CQRCode_decode_three_color(frame,test=True)
#         cv2.imshow('test',frame)

#         cv2.imshow('test_B',img_B)

#         cv2.imshow('test_R',img_R)
#         cv2.imshow('test_G',img_G)

#         print(data)


#         if(R_data==None and G_data==None and B_data==None):
#             total-=1

#         if(data!=None):
#             cnt+=1

        
#         #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
#         #cv2.imshow('test_R',img_R2)
#         #
#         #cv2.imshow('test',img)
#         #cv2.waitKey(5000)
        


#     print("total:",total)
#     print("success:",cnt)


# elif MODE==4:
#     tests=os.listdir("tests")
#     total=len(tests)
#     for img in tests:
#         frame=cv2.imread("tests/"+img)
#         data=decoder.QRCode_decode(frame)
#         cv2.imshow('test',frame)


#         print(data)

#         if(data!=None):
#             cnt+=1

        
#         #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
#         #cv2.imshow('test_R',img_R2)
#         #
#         #cv2.imshow('test',img)
#         #cv2.waitKey(5000)
        


#     print("total:",total)
#     print("success:",cnt)
# elif MODE == 5:
#     frame=cv2.imread('test6.jpg')
#     img_B,img_G,data=decoder.CQRCode_decode_test_BG(frame)
#     cv2.imshow('test',frame)

#     cv2.imshow('test_G',img_G)

#     cv2.imshow('test_B',img_B)
#     print(data)
#     #ret,img_R=cv2.threshold(img_R,220, 255,cv2.THRESH_BINARY)
#     #cv2.imshow('test_R',img_R2)
#     #
#     #cv2.imshow('test',img)
#     cv2.waitKey(0)

# elif MODE == 6:


#     cap=cv2.VideoCapture(0)


#     #cap.set(cv2.CAP_PROP_BRIGHTNESS,0.5)
#     while(True):
#         ret,frame=cap.read()
#         img_R,img_G,img_B,data=decoder.CQRCode_decode_three_color(frame,test=True)
#         cv2.imshow('test',frame)

#         cv2.imshow('test_B',img_B)

#         cv2.imshow('test_R',img_R)
#         cv2.imshow('test_G',img_G)

#         print(data)
#         cv2.waitKey(500)





# else:

#     cap=cv2.VideoCapture(0)
#     exposure = -5
#     cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3.0) # 先打开自动曝光
#     # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1.0) # 再关闭自动曝光
#     # cap.set(cv2.CAP_PROP_EXPOSURE, exposure) # 最后设置曝光参数


#     #cap.set(cv2.CAP_PROP_BRIGHTNESS,0.5)
#     while(True):
        
#         ret,frame=cap.read()
#         out=decoder.adjust_light(frame)
        
#     #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     #     gray=np.float16(gray)
#     #     weight=0.
#     #     weight= gray- np.mean(gray, axis = 0)  # zero-center
#     #     weight /= np.std(gray, axis = 0)   # normalize
#     #     weight+=1
#     #     # print(weight)
#     #     mid = 0.5
#     #     gray=np.uint8((gray*weight).clip(0,255))
#     #     mean = np.mean(gray)
        
        
#     #     _, mask = cv2.threshold(gray, mean, 255, cv2.THRESH_BINARY)  #找到亮度比较高的区域
#     #     mask_inv = cv2.bitwise_not(mask)
#     # # 在原图中仅保留亮区域
#     #     image_cropped = cv2.bitwise_and(frame, frame, mask=mask)


#     #     mean = gray[np.nonzero(mask_inv)].mean()
#     #     print(mean)
#     #     gamma = math.log(mid*255)/math.log(mean)
#     #     img_gamma1 = np.power(frame, gamma).clip(0,255).astype(np.uint8)

#         cv2.imshow('orig',frame)
#         cv2.imshow('test',out)

#         cv2.waitKey(500)



def add_white_frame(square_image,occupy_image_width=1060,occupy_image_height=1060,screen_width=1920,screen_height=1080):
    # 获取正方形图像的尺寸
    square_height, square_width = square_image.shape[:2]

    # occupy_image_size=1060

    res_img_width=int(square_width/occupy_image_width*screen_width)
    res_img_height=int(square_height/occupy_image_width*screen_height)


    # 计算中心位置
    y_offset = int((res_img_height - square_height) // 2)
    x_offset = int((res_img_width - square_width) // 2)

    # 创建1920x1080的白色背景图像
    res_img = np.ones((res_img_height, res_img_width, 3), dtype=np.uint8) * 255  # 白色背景
    

    #按照比例缩放

    # 将正方形图像放置在白色背景中
    res_img[y_offset:y_offset + square_height, x_offset:x_offset + square_width] = square_image
    return res_img




# qrcode_type=7     #rgb
qrcode_type=3  #rg


# 生成数据帧
# use_compress=True


# encoder=Encoder(version=4,qrcode_type=qrcode_type,)
# data='132'*100
# cqrcodes=encoder.generate_data_cqrcodes(data)
# for i,cqrcode in enumerate(cqrcodes):
#     cqrcode=add_white_frame(cqrcode)
#     cv2.imwrite(f'test2/{i}.jpg',cqrcode)
#     cv2.imshow('test',cqrcode)
#     cv2.waitKey(0)


#解码数据帧

decoder=Decoder()
img_paths=[os.path.join('test2',filename) for filename in os.listdir('test2')]
# img_paths=[os.path.join('tests',filename) for filename in os.listdir('tests')]
imgs=[]
# data_frames=[]
decoded_frame_dict={}
for img_path in img_paths:
    img=cv2.imread(img_path)
    data_frame=decoder.CQRCode_decode(img,qrcode_type)
    decoded_frame=decoder.decode_data_frame(data_frame)
    decoded_frame_dict[decoded_frame['seq_num']]=decoder.decode_data_frame(data_frame)



data=decoder.reassemble_data_frames(decoded_frame_dict,3)


print(data)




#生成控制帧

# encoder=Encoder(version=4,qrcode_type=qrcode_type,)

# decoded_frame_dict={1:'',2:''}
# control_frame=encoder.generate_control_qrcode(status_code=1,total_frames=3,decoded_frame_dict=decoded_frame_dict)
# control_frame=add_white_frame(control_frame)
# cv2.imshow('test',control_frame)
# cv2.waitKey(0)
# cv2.imwrite('test2/control_frame.jpg',control_frame)






#解码控制帧

# control_frame_img=cv2.imread('test2/control_frame.jpg')

# control_frame=decoder.QRCode_decode(control_frame_img)

# control_frame_dict=decoder.decode_control_frame(control_frame)
# decoder.decode_lack_num(control_frame_dict['lack_num'])

# print(control_frame_dict)






import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np




class Decoder:
    def __init__(self) -> None:
        pass



    def QRCode_decodeDisplay(self,img,win_name):
        # 转为灰度图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)
        for barcode in barcodes:
            # 提取二维码的位置
            (x, y, w, h) = barcode.rect
            # 用边框标识出来在视频中 (0, 255, 0), 2 是rgb颜色；边框的宽度，这边是2
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 字符串转换
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # 在图像上面显示识别出来的内容
            text = "{}".format(barcodeData)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # 打印识别后的内容
            print("[扫描结果] 二维码类别： {0} 内容： {1}".format(barcodeType, barcodeData))
        cv2.imshow(win_name, img)



    def QRCode_decode(self,img):
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(img)
        data_list=[]
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            data_list.append(barcodeData)
        if(len(data_list)>0):
            return data_list[0]
        return None

        
    
    def QRCode_decodeAll(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)
        data_list=[]
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            data_list.append(barcodeData)

        return data_list
    

    def CQRCode_decode(self,img):
        img_R=self.ProcessCQRCode_R(img.copy())
        img_G=self.ProcessCQRCode_G(img.copy())
        
        R_data =self.QRCode_decode(img_R)
        G_data =self.QRCode_decode(img_G)

        res=None
        if(R_data!=None and G_data!=None):
            res=G_data+R_data
        
        print('R:',R_data)
        print('G:',G_data)

        return res
    
    def CQRCode_decode_test(self,img):
        img_R=self.ProcessCQRCode_R(img.copy())
        img_G=self.ProcessCQRCode_G(img.copy())
        

        R_data =self.QRCode_decode(img_R)
        G_data =self.QRCode_decode(img_G)

        res=None
        if(R_data!=None and G_data!=None):
            res=G_data+R_data
        
        print('R:',R_data)
        print('G:',G_data)

        return img_R,img_G,res
    

    def Light_adjust(self,img):
        img=img.astype(np.int32)
        test=img-(255-img)*2
        #print(img)
    
        img2=cv2.normalize(test, None, 0, 255, cv2.NORM_MINMAX)
    
        test=test.astype(np.uint8)
        

        # for i in range(len(img)):
        #     for j in range(len(img[i])):
        #         img[i][j]=np.uint8(max(0,min(255,img[i][j]*alpha+belta)))
        #cv2.imwrite('test.jpg',test)
        return test


    def ProcessCQRCode_R(self,img):
        # img[:,:,0]=np.maximum(img[:,:,0],img[:,:,2])
        # img[:,:,1]=np.maximum(img[:,:,1],img[:,:,2])
        img[:,:,0]=img[:,:,2]
        img[:,:,1]=img[:,:,2]


        #cv2.imshow('img_1',img)

        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('img_2',gray)
        #img_R=cv2.bilateralFilter(gray,  7, 150, 10)



        #ret,img_R=cv2.threshold(gray,210, 255,cv2.THRESH_BINARY)
        #img_R=cv2.equalizeHist(img_R)

        return gray



    

    def ProcessCQRCode_G(self,img):
        img[:,:,0]=img[:,:,1]
        img[:,:,2]=img[:,:,1]

        #cv2.imshow('img_G',img)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #img_G=cv2.bilateralFilter(gray,  7, 150, 10)



        #ret,img_G=cv2.threshold(gray,180, 255,cv2.THRESH_BINARY)
        #img_G=cv2.equalizeHist(img_G)


        return gray


 

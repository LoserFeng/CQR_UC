from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication,QMainWindow,QFileDialog,QGraphicsPixmapItem,QGraphicsScene)

from PyQt5.QtGui import QPixmap,QImage

from PyQt5.QtCore import *
from sender_ui import Ui_MainWindow

import sys
import time
import os

import cv2
import re

import onnxruntime as ort

from utils import plot_one_box,_make_grid,cal_outputs,post_process_opencv,infer_img

import numpy as np




WAIT_TIME=50






class MainUI(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setupUi(self)

        self.inputText.setPlaceholderText('请输入想要传输的字符串')

        self.exitButton.clicked.connect(self.onClick_exitButton)   #退出按钮
        self.sendButton.clicked.connect(self.onClick_sendButton)   #传输信息的按钮
        


    
    def onClick_exitButton(self):
        sender = self.sender()
        print(sender.text() + ' 按钮被按下')
        app = QApplication.instance()
        # 退出应用程序
        app.quit()



    def onClick_sendButton(self):
        self.stackedWidget.setCurrentIndex(1)
        self.send_procession()
        

    

    def showImg(self,seq):
         
        pix=cv2.imread(self.imgs[seq])
        cv2.imshow('CQRCode_win',pix)

        self.Order_Label.setText(str(seq))
        
        


         









            

    def send_procession(self):

        transmission_text=self.inputText.toPlainText()
        print("input text is :%s"%transmission_text)


        print('正在执行二维码生成程序')
        tt=os.system('dotnet ./CQRCode/TEST.dll %s'%(transmission_text))
        print(tt)

        if tt<0:
            print("tt  < 0")
            app=QApplication.instance()
            app.quit()
        


        
        cv2.namedWindow('CQRCode_win',cv2.WINDOW_FULLSCREEN)
        wait_img=cv2.imread('./assets/wait.jpg')
        print(wait_img.shape)
        cv2.imshow('CQRCode_win',wait_img)


        self.Order_Label.setText('')

        files=os.listdir('./assets')


        imgs=[]


        for i,fileName in enumerate(files):
            res=re.match(r'CQRCode_[\d]+.jpg',fileName)
            if(res==None):
                print('the file\'s name %s does not match'%fileName)
                continue
            filePath='./assets/'+fileName
            imgs.append(filePath)



        
        self.imgs=imgs
        QApplication.processEvents()

        sendthd=SendThread(imgs)
        sendthd.show_sig.connect(self.showImg)
        sendthd.finish_sig.connect(self.finish)
        sendthd.start()
        #sendthd.setPriority(QThread.LowPriority)
        #sendthd.wait()
        sendthd.exec()

        


    def finish(self):
            #处理传送完结事项
        os.system('rm  ./assets/CQRCode_*.jpg ')
        self.inputText.setPlainText('')
        self.inputText.setPlaceholderText('请输入想要传输的字符串')
        self.Order_Label.setText('')
        cv2.destroyAllWindows()
        
        self.stackedWidget.setCurrentIndex(0)







class SendThread(QThread):
    show_sig = pyqtSignal(int)
    finish_sig=pyqtSignal(int)

    def __init__(self,imgs):
        super(SendThread, self).__init__()
        self.imgs=imgs

    def run(self):
        model_pb_path = "./weights/flag_detect.onnx"
        so = ort.SessionOptions()
        net = ort.InferenceSession(model_pb_path, so)
        
        # 标签字典
        dic_labels= {0:'ready_flag',
                1:'reading_flag'}
        
        # 模型参数
        model_h = 320
        model_w = 320
        nl = 3
        na = 3
        stride=[8.,16.,32.]
        anchors = [[10, 13, 16, 30, 33, 23], [30, 61, 62, 45, 59, 119], [116, 90, 156, 198, 373, 326]]
        anchor_grid = np.asarray(anchors, dtype=np.float32).reshape(nl, -1, 2)
        
        video = 0
        cap = cv2.VideoCapture(video)
        flag_det = True   #是否开始检测

        status=None


        seq=0
        t1 = time.time()
        
        while True:
            success, img0 = cap.read()
            if success:
                t2 = time.time()
                
                if( t2-t1>WAIT_TIME):
                    print('超出时间限制，接收端无反应，退出!')
                    break
                
                if flag_det:
                    
                    det_boxes,scores,ids = infer_img(img0,net,model_h,model_w,nl,na,stride,anchor_grid,thred_nms=0.4,thred_cond=0.5)

                    if(len(ids)>0):
                        print('detect targets: ',ids)

                        if status==ids[0]:
                            continue
                        elif status!=ids[0]:
                            status=ids[0]
                            if status==0:
                                if seq>=len(self.imgs):
                                    print('信息发送完成！')
                                    break
                                self.show_sig.emit(seq)

                                print(time.ctime(),'detect the status ready')

                            elif status==1:
                                t1 = time.time()
                                #self.showImg(imgs[seq])
                                print(time.ctime(),'detect the status reading')
                                seq+=1
                                
        
            cv2.waitKey(400)

                
        cap.release()
        self.finish_sig.emit(1)
        




        



def main():
    print("hello i'm sender!")
    app=QApplication(sys.argv)

    main=MainUI()

    main.stackedWidget.setCurrentIndex(0)
    #main.showFullScreen()
    main.show()

    sys.exit(app.exec_())
























if __name__=="__main__":
    main()
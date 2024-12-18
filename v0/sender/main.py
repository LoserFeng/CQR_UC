from PyQt5.QtWidgets import ( QApplication,QMainWindow,QFileDialog,QGraphicsPixmapItem,QGraphicsScene)



from PyQt5.QtCore import *
from sender_ui import Ui_MainWindow

import sys
import time
import os

import cv2
import re


from detect import Detector
from CQRCode import Decoder,Encoder
from utils import generate_data
import numpy as np




WAIT_TIME=50  #超出多少时间退出


WAIT_KEY_TIME=10

SEND_INTERVAL=400 #发送的间隔

TEST=False

LINUX_FLAG:bool=False

QRCODE_VERSION:int=4  #version 为1-40
QRCODE_TYPE:int = 3  #exp: 011 RG   111  RGB  1000 white

ERROR_CORRECT_LEVEL:str = 'L'
USE_COMPRESS=1

FILL_8k_data=False
FILL_4k_data=True





# task_id=0  #修改
# select_id=0  #用于选择每个task_dir下具体是哪个种类的生成二维码方式
 
# select_list=os.listdir(os.path.join('CQRCode',task_list[task_id]))
# select_list.sort()
# assert select_id<=len(select_list)

# target_dir=os.path.join('CQRCode',task_list[task_id],select_list[select_id])


import argparse



class MainUI(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setupUi(self)

        self.inputText.setPlaceholderText('请输入想要传输的字符串')

        self.exitButton.clicked.connect(self.onClick_exitButton)   #退出按钮
        self.sendButton.clicked.connect(self.onClick_sendButton)   #传输信息的按钮
        # self.detector=Detector()
        # self.decoder=Decoder()
        


    
    def onClick_exitButton(self):
        sender = self.sender()
        print(sender.text() + ' 按钮被按下')
        app = QApplication.instance()
        # 退出应用程序
        app.quit()



    def onClick_sendButton(self):

        self.send_procession()
        

    

    def showImg(self,pix=None,filepath=None):
        

        if(pix is None):
            pix=cv2.imread(filepath)
        #pix=cv2.resize(pix,(480,480))

        if TEST:
            cv2.imshow('test',pix)
        else:
            cv2.imshow('CQRCode_win',pix)
        

        
        


         









            

    def send_procession(self):

        transmission_text=self.inputText.toPlainText()
        # print("input text is :%s"%transmission_text)
        if(FILL_8k_data):
            transmission_text=generate_data()
        elif(FILL_4k_data):
            transmission_text=generate_data(4000)


        print('正在执行二维码生成程序')



        if TEST:
            cv2.namedWindow('test',cv2.WINDOW_GUI_NORMAL)
        else:
            cv2.namedWindow('CQRCode_win', cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow('CQRCode_win', 0,0)
            cv2.setWindowProperty("CQRCode_win", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        #print(wait_img.shape)
        #wait_img=cv2.resize(wait_img,(480,480))
        #wait_img=cv2.imread('./wait.jpg')
        # self.showImg('./wait.jpg')  #这个改成receiver显示








        

        QApplication.processEvents()


        self.send(transmission_text)



        self.finish()

        


    def finish(self):
            #处理传送完结事项

        self.inputText.setPlainText('')
        self.inputText.setPlaceholderText('请输入想要传输的字符串')

        cv2.destroyAllWindows()
        




    def send(self,transmission_data):

        
        video = 0
        cap = cv2.VideoCapture(video)

        loop_flag=True
        fin_flag=False

        status=0
        total_frames=0


        send_all_data=False
        seq_num=-1
        send_list=[]
        send_rounds=0
        t1 = time.time()
        send_data_flag=False

        encoder=Encoder(version=QRCODE_VERSION,qrcode_type=QRCODE_TYPE,error_correct_level=ERROR_CORRECT_LEVEL,use_compress=USE_COMPRESS)
        decoder=Decoder()
        t_start_make=time.time()
        print('begin to generate CQRCodes')
        data_frame_imgs=encoder.generate_data_cqrcodes(transmission_data)
        t_end_make=time.time()
        
        print(f'make {len(data_frame_imgs)} CQRCodes completed successfully! use time {t_end_make-t_start_make} ')
        self.showImg(filepath='./wait.jpg')

        print('status:0')


        while loop_flag:
            success, img0 = cap.read()
            if success:
                t2 = time.time()
                
                if( t2-t1>WAIT_TIME):
                    print('超出时间限制，接收端无反应，退出!')
                    loop_flag=False


                if(status==0):



                    qrcode_data=decoder.QRCode_decode(img0)
                    if qrcode_data!=None:
                        control_frame=decoder.decode_control_frame(qrcode_data)
                        if(control_frame!=None):
                            if(control_frame['status_code']!=0):
                                print(f'control_frame status_code wrong:{control_frame["status_code"]} expected 1')
                            else:
                                # send_list=decoder.decode_lack_num(control_frame['lack_num'])
                                # send_data_flag=True
                                
                                control_frame_img=encoder.generate_control_qrcode(status_code=status,total_frames=len(data_frame_imgs))
                                self.showImg(control_frame_img)
                                status=1
                                t1 = time.time()

                elif(status==1):
                    # if not send_all_data and send_data_flag:
                    #     for idx in send_list:   #发送一遍二维码图片
                    #         self.showImg(data_frame_imgs[idx])
                    #         cv2.waitKey(SEND_INTERVAL)
                    #     send_all_data=True
                    #     send_data_flag=False
                    #     t1 = time.time()
                    #     print(f'finish send_rounds{send_rounds}')
                    #     continue

                    qrcode_img=decoder.QRCode_decode(img0)
                    if(qrcode_img!=None):
                        control_frame=decoder.decode_control_frame(qrcode_img)
                        if(control_frame!=None):
                            if(control_frame['status_code']==2):
                                print('receiver has received all data')
                                status=control_frame['status_code']
                                control_frame_img=encoder.generate_control_qrcode(status_code=status)
                                self.showImg(control_frame_img)
                                t1=time.time()




                            elif(control_frame['status_code']==1):


                                _seq_num=control_frame['seq_num']
                                if(_seq_num!=seq_num):
                                    seq_num+=1
                                    self.showImg(data_frame_imgs[seq_num])
                                    print(f'show idx：{seq_num}')
                               

                                t1=time.time()
                            else:
                                print(f'warning:get status_code{control_frame["status_code"]} ,expected 1 or 2')

                elif(status==2):
                    qrcode_img=decoder.QRCode_decode(img0)
                    if(qrcode_img!=None):
                        control_frame=decoder.decode_control_frame(qrcode_img)
                        if(control_frame!=None):
                            if(control_frame['status_code']==3):
                                status=3
                                t1=time.time()
                            else:
                                print(f'receive status code{control_frame["status_code"]}')
                            
                else:
                    loop_flag=False
                    print('完成传输')
                    


                



                                
        
            cv2.waitKey(WAIT_KEY_TIME)

                
        cap.release()







        



def main():
    print("hello i'm sender!")
    app=QApplication(sys.argv)

    main=MainUI()


    if(TEST):
        main.show()
    else:
        main.showFullScreen()

    sys.exit(app.exec_())













def parse_args():
    parser = argparse.ArgumentParser(description="Command line argument parser for the script.")

    parser.add_argument('--wait_time', type=int, default=50, help='Time to wait before exiting.')
    parser.add_argument('--wait_key_time', type=int, default=10, help='Time to wait for a key press.')
    parser.add_argument('--send_interval', type=int, default=400, help='Interval between sends.')
    parser.add_argument('--test', action='store_true', help='Enable test mode.')
    parser.add_argument('--linux_flag', action='store_true', help='Flag for Linux environment.')
    parser.add_argument('--qrcode_version', type=int, default=4, help='Version of the QR code (1-40).')
    parser.add_argument('--qrcode_type', type=int, default=3, help='Type of the QR code (e.g., 011 RG, 111 RGB, 1000 white).')
    parser.add_argument('--error_correct_level', type=str, default='L', help='Error correction level for the QR code.')
    parser.add_argument('--use_compress', type=int, default=1, help='Flag to use compression.')

    return parser.parse_args()










if __name__=="__main__":
    args = parse_args()
    #更新参数
    WAIT_TIME=args.wait_time
    WAIT_KEY_TIME=args.wait_key_time
    SEND_INTERVAL=args.send_interval
    TEST=args.test
    LINUX_FLAG=args.linux_flag
    QRCODE_VERSION=args.qrcode_version
    QRCODE_TYPE=args.qrcode_type
    ERROR_CORRECT_LEVEL=args.error_correct_level
    USE_COMPRESS=args.use_compress
    main()
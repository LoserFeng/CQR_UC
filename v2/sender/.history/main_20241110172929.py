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

SEND_INTERVAL=300 #发送的间隔  #400

TEST=True

LINUX_FLAG:bool=False

QRCODE_VERSION:int= 9  #version 为1-40
QRCODE_TYPE:int =   #011 RG     111  RGB  1000 white

ERROR_CORRECT_LEVEL:str = 'M'
USE_COMPRESS=1  #压缩等级， 为0的时候代表是False 

FILL_8k_data=True
FILL_4k_data=False





# task_id=0  #修改
# select_id=0  #用于选择每个task_dir下具体是哪个种类的生成二维码方式
 
# select_list=os.listdir(os.path.join('CQRCode',task_list[task_id]))
# select_list.sort()
# assert select_id<=len(select_list)

# target_dir=os.path.join('CQRCode',task_list[task_id],select_list[select_id])




class MainUI(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setupUi(self)

        self.inputText.setPlaceholderText('请输入想要传输的字符串')

        self.exitButton.clicked.connect(self.onClick_exitButton)   #退出按钮
        self.sendButton.clicked.connect(self.onClick_sendButton)   #传输信息的按钮
        self.detector=Detector()
        self.decoder=Decoder()
        


    
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
        if(FILL_4k_data):
            transmission_text=generate_data(5000)


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
        seq=0
        send_list=[]
        send_rounds=0
        t1 = time.time()
        send_data_flag=False
        parity_code=0
        receiver_parity_code=0
        lack_num_list=[]
        lack_num_len=128

        encoder=Encoder(version=QRCODE_VERSION,qrcode_type=QRCODE_TYPE,error_correct_level=ERROR_CORRECT_LEVEL,use_compress=USE_COMPRESS)
        decoder=Decoder()
        t_start_make=time.time()
        print('begin to generate CQRCodes')
        data_frame_imgs=encoder.generate_data_cqrcodes(transmission_data)
        t_end_make=time.time()
        
        print(f'make {len(data_frame_imgs)} CQRCodes completed successfully! use time {t_end_make-t_start_make} ')  #435帧

        control_frame_imgs=encoder.generate_control_qrcodes(status_code=status,parity_code=parity_code,total_frames=len(data_frame_imgs))
        assert len(control_frame_imgs)==1
        control_frame_img=control_frame_imgs[0]
        
        
        self.showImg(control_frame_img)
        parity_code^=1

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
                        control_frame_dict=decoder.decode_control_frame(qrcode_data)
                        if(control_frame_dict!=None):
                            print(f'receive control_frame:{control_frame_dict}')

                            if(control_frame_dict['parity_code']!=receiver_parity_code):
                                continue
                            else:
                                receiver_parity_code^=1  #0->1
                            if(control_frame_dict['status_code']!=0):  #第一帧是1 ？
                                print(f'control_frame status_code wrong:{control_frame_dict["status_code"]} expected 0')
                            else:  #第一次默认发送全部，不需要进入阶段1
                                # send_list=decoder.decode_lack_num_list(control_frame_dict['lack_num'])
                                send_list=list(range(len(data_frame_imgs)))
                                send_data_flag=True
                                status=2
                                t1 = time.time()

                elif(status==1):
                    
                    qrcode_data=decoder.QRCode_decode(img0)
                    if qrcode_data!=None:
                        control_frame_dict=decoder.decode_control_frame(qrcode_data)
                        if(control_frame_dict!=None):
                            print(f'receive control_frame:{control_frame_dict}')
                            if(control_frame_dict['parity_code']!=receiver_parity_code):
                                continue
                            else:
                                receiver_parity_code^=1
                            if(control_frame_dict['status_code']!=1):
                                print(f'control_frame status_code wrong:{control_frame_dict["status_code"]} expected 1')

                            else:
                                lack_num=control_frame_dict['lack_num']
                                lack_num_list.append(control_frame_dict['lack_num'])
                                if(1<<lack_num_len-1)&lack_num:  #tule
                                    send_list=decoder.decode_lack_num_list(lack_num_list)
                                    lack_num_list=[]
                                    print(f'sender has get all lack_num len(lack_num_list):{len(lack_num_list)}')
                                    status=2
                                    send_data_flag=True
                                    send_all_data=False
                                else:
                                    control_frame_imgs=encoder.generate_control_qrcodes(status_code=status,parity_code=parity_code,send_rounds=send_rounds,total_frames=len(data_frame_imgs))
                                    assert len(control_frame_imgs)==1
                                    self.showImg(control_frame_imgs[0])
                                    parity_code^=1
                                    

                                
                               
                                t1 = time.time()




                elif(status==2):
                    if not send_all_data and send_data_flag:
                        for idx in send_list:   #发送一遍二维码图片
                            self.showImg(data_frame_imgs[idx])
                            cv2.waitKey(SEND_INTERVAL)
                        send_all_data=True
                        send_data_flag=False
                        t1 = time.time()
                        print(f'finish send_rounds{send_rounds}')
                        continue

                    qrcode_img=decoder.QRCode_decode(img0)
                    if(qrcode_img!=None):
                        control_frame_dict=decoder.decode_control_frame(qrcode_img)
                        if(control_frame_dict!=None):
                            print(f'receive control_frame:{control_frame_dict}')
                            if(control_frame_dict['parity_code']!=receiver_parity_code):
                                continue
                            else:
                                receiver_parity_code^=1  # 1->0
                            if(control_frame_dict['status_code']==3):
                                print('receiver has received all data')
                                lack_num=control_frame_dict['lack_num']
                                assert(lack_num==(1<<lack_num_len-1))
                                status=3  # 3
                                print(f'status{status}')
                                

                                control_frame_imgs=encoder.generate_control_qrcodes(status_code=status,parity_code=parity_code,send_rounds=send_rounds)
                                assert len(control_frame_imgs)==1
                                
                                self.showImg(control_frame_imgs[0])
                                parity_code^=1
                                t1=time.time()
                                send_data_flag=False



                            elif(control_frame_dict['status_code']==1):
                                print(f'receiver show send_rounds:{control_frame_dict["send_rounds"]},time:{time.time()}')
                                if(send_rounds==control_frame_dict['send_rounds']):  #如果不是新的发送轮次，说明还没有进入到下一个发送轮次
                                    send_data_flag=False
                                    continue
                                print('receiver not received all data')
                                status=1
                                print('status 1')

                                send_rounds=control_frame_dict['send_rounds']  #根据接收端更新自己的send_rounds

                                lack_num=control_frame_dict['lack_num']
                                lack_num_list.append(control_frame_dict['lack_num'])
                                if(1<<lack_num_len-1)&lack_num:   #tule
                                    send_list=decoder.decode_lack_num_list(lack_num_list)
                                    lack_num_list=[]
                                    print(f'sender has get all lack_num len(lack_num_list):{len(lack_num_list)}')
                                    status=2
                                    print('status 2')
                                    send_data_flag=True
                                    send_all_data=False
                                else:
                                    control_frame_imgs=encoder.generate_control_qrcodes(status_code=status,parity_code=parity_code,send_rounds=send_rounds,total_frames=len(data_frame_imgs))
                                    assert len(control_frame_imgs)==1
                                    self.showImg(control_frame_imgs[0])
                                    parity_code^=1


                            
                                t1 = time.time()







                                # lack_num=control_frame_dict['lack_num']
                               
                                # send_list=decoder.decode_lack_num(lack_num)
                                # print(f'lack:{send_list}')
                                # assert(len(send_list)>=0)
                                # send_all_data=False
                                # send_rounds=control_frame_dict['send_rounds']
                                # send_data_flag=True
                                # t1=time.time()
                            else:
                                print(f'warning:get status_code{control_frame_dict["status_code"]} ,expected 1 or 2')

                elif(status==3):
                    qrcode_img=decoder.QRCode_decode(img0)
                    if(qrcode_img!=None):
                        control_frame_dict=decoder.decode_control_frame(qrcode_img)
                        if(control_frame_dict!=None):
                            print(f'receive control_frame:{control_frame_dict}')
                            if(control_frame_dict['parity_code']!=receiver_parity_code):
                                continue
                            else:
                                receiver_parity_code^=1

                            if(control_frame_dict['status_code']==4):
                                status=4
                                t1=time.time()
                            else:
                                print(f'receive status code{control_frame_dict["status_code"]}')
                            
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
























if __name__=="__main__":
    main()
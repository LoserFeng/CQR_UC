
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication,QMainWindow)
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import *
from receiver_ui import Ui_MainWindow
from CQRCode import Decoder,Encoder
import sys
import time
from utils import get_last_seq_num


import cv2






TEST=True


WAIT_TIME=100
WAIT_KEY_TIME=10
WAIT_TO_END_TIME=1000





class receiver:
    def __init__(self):
        print('receiver created')
    def receive_procession(self):
        print('begin to receive')




class MainUI(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setupUi(self)

        self.receiver=receiver()

        self.exitButton.clicked.connect(self.onClick_exitButton)   #退出按钮

        self.receiveButton.clicked.connect(self.OnClick_receiveButton)




        


    
    def onClick_exitButton(self):
        sender = self.sender()
        print(sender.text() + ' 按钮被按下')
        app = QApplication.instance()
        # 退出应用程序
        app.quit()



    def OnClick_receiveButton(self):
        sender = self.sender()
        print(sender.text() + ' 按钮被按下')

        res,data=self.receive_procession()

        if(res):
            self.receiveLabel.setText(data)
        else:
            self.receiveLabel.setText("传输失败")



    def showImg(self,pix=None,filepath=None):
        if(pix is None): 
            pix=cv2.imread(filename=filepath)
        if(TEST):
            cv2.imshow('test',pix)
        else:
            cv2.imshow('flag_win',pix)






        



    def receive_procession(self):
        print('begin to receive')
        res=False
        data=None
        wait_time=WAIT_TIME
        if TEST:
            cv2.namedWindow('test',cv2.WINDOW_GUI_NORMAL)
        else:
            cv2.namedWindow('flag_win', cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow('flag_win', 0,0)
            cv2.setWindowProperty("flag_win", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        #self.showImg('./assets/ready.png')

        video = 0
        cap = cv2.VideoCapture(video)
        t1 = time.time()
        encoder=Encoder(version=1,qrcode_type=0,error_correct_level='H',use_compress=False)
        decoder=Decoder(test=TEST)
        # detector=Detector()


        loop_flag=True
        # seq=0
        status=0
        err_cnt=0  #识别错误的二维码数量
        all_cnt=0  #收到的二维码图片数量
        # send_rounds=0  #发送轮次
        end_frame_num=0 #这一轮中最后一帧是哪个
        seq_num=0


        time_start=0
        time_end=0

        

        decoded_frame_dict={}
        total_frames=0
        qrcode_type=0
        use_compress=False
        last_frame_cnt=-1

        control_frame_img=encoder.generate_control_qrcode(status_code=status,total_frames=total_frames)
        self.showImg(control_frame_img)

        # self.showImg(filepath='./assets/wait.jpg')

        print('status:0')


        while(loop_flag):
            success, img0 = cap.read()
            if success:
                t2 = time.time()
                if( t2-t1>wait_time):
                    print('超出时间限制，发送端无反应，退出!')
                    break


                if status==0:
                    qrcode_data=decoder.QRCode_decode(img0)
                    if(qrcode_data!=None):
                        control_frame_dict=decoder.decode_control_frame(qrcode_data)
                        if(control_frame_dict!=None):
                            if(control_frame_dict['status_code']==0):
                                total_frames=control_frame_dict['total_frames']
                                qrcode_type=control_frame_dict['qrcode_type']
                                use_compress=control_frame_dict['use_compress']

                                status=1
                                print(f'status: {status}')


                                t1=time.time()
                                time_start=time.time()
                                
                            else:
                                print(f'detect status_code:{control_frame_dict["status_code"]} from sender but expected status_code 0')

                elif status==1:

                    all_cnt+=1
                    CQRCode_data=decoder.CQRCode_decode(img0,qrcode_type=qrcode_type)


                    if(CQRCode_data!=None ):
                        data_frame=decoder.decode_data_frame(CQRCode_data)
                        if(data_frame!=None):
                            if seq_num==data_frame['seq_num']:
                                continue
                            decoded_frame_dict[data_frame['seq_num']]=data_frame
                            seq_num+=1
                            if(seq_num==total_frames):
                                status=2
                                print('status: 2')
                                control_img=encoder.generate_control_qrcode(status_code=status,total_frames=total_frames,seq_num=seq_num)
                                print('已经收到了所有二维码')
                                
                                self.showImg(control_img)
                                print(f'show img {seq_num} ')
                                
                            else:
                                control_img=encoder.generate_control_qrcode(status_code=1,total_frames=total_frames,seq_num=seq_num)
                                self.showImg(control_img)
                                print(f'show img {seq_num} ')
    
                        else:
                            # 这个要算进 
                            print(f'receive data {CQRCode_data} but not able to decode as dataframe ?这个还没算进err_cnt !')
                    else:
                        err_cnt+=1
                elif status==2:
                    # ids=detector.identify(img0)
                    qrcode_data=decoder.QRCode_decode(img0)
                    if(qrcode_data!=None):
                        control_frame=decoder.decode_control_frame(qrcode_data)
                        if(control_frame!=None):
                            if(control_frame['status_code']==2):
                                status=3
                                print('进入Status 3')
                                control_frame_img=encoder.generate_control_qrcode(status_code=status)
                                self.showImg(control_frame_img)
                                t1=time.time()
                                time_end=time.time()
                                cv2.waitKey(WAIT_TO_END_TIME)


                    
                else:
                    print('status 3')
                    loop_flag=False
                    cv2.destroyAllWindows()
                    print(f'err_cnt:{err_cnt}')
                    print(f'all_cnt:{all_cnt}')
                    print(f'detect_accur:{err_cnt/all_cnt*1.0}')
                    print(f'transmission_time:{time_end-time_start}')
                    print(f'send_rounds:{send_rounds}')
                    
                    data=decoder.reassemble_data_frames(decoded_frame_dict,use_compress=use_compress,total_frames_expected=total_frames)


                    print(f'speed:{len(data)/(time_end-time_start)*1.0} byte/s')
                    res=True

            cv2.waitKey(WAIT_KEY_TIME)
        cv2.destroyAllWindows()
        #WAIT_TIME=50

        print(decoded_frame_dict.keys())
        return res,data
            
                


            






        



def main():
    print("hello i'm receiver!")
    app=QApplication(sys.argv)

    main=MainUI()


    #main.showFullScreen()
    if(TEST):
        main.show()
    else:
        main.showFullScreen()

    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
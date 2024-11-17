
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication,QMainWindow)
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import *
from receiver_ui import Ui_MainWindow
from CQRCode import Decoder,Encoder
import sys
import time
from utils import get_last_seq_num,log_experiment_result,save_img

import queue
import cv2






TEST=True


WAIT_TIME=50
WAIT_KEY_TIME=50
WAIT_TO_END_TIME=2000





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
        send_rounds=0  #发送轮次
        end_frame_num=0 #这一轮中最后一帧是哪个
        parity_code=0  #奇偶码，用于防止控制帧相同导致的传输问题
        sender_parity_code=0
        save_flag=False
        


        time_start=0
        time_end=0

        

        decoded_frame_dict={}
        total_frames=0
        qrcode_type=0
        use_compress=False
        last_frame_cnt=-1
        send_control_frame_flag=False

        control_frame_img_send_queue=queue.Queue()



        self.showImg(filepath='./assets/wait.jpg')

        print('status:0')


        while(loop_flag):



            # 发送阶段
            if not  control_frame_img_send_queue.empty() and send_control_frame_flag:
                img=control_frame_img_send_queue.get()
                print('send one control_frame_img')
                self.showImg(img)
                parity_code=parity_code^1  #每发一帧图像之后都要取反
                send_control_frame_flag=False


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
                            print(f'receive control_frame:{control_frame_dict}')
                            if(control_frame_dict['parity_code']!=sender_parity_code):
                                continue
                            else:
                                sender_parity_code^=1
                                if(control_frame_dict['status_code']==0):
                                    total_frames=control_frame_dict['total_frames']
                                    qrcode_type=control_frame_dict['qrcode_type']
                                    use_compress=control_frame_dict['use_compress']


                                    # if(send_parity_code!=parity_code):
                                    #     print(f'send_parity_code is not right sender:{send_parity_code},receiver:{parity_code}')

                                    # lack_num=encoder.get_lack_num(total_frames,decoded_frame_dict)
                                    end_frame_num=total_frames-1  #得到最后一帧的标号
                                    
                                    control_frame_imgs=encoder.generate_control_qrcodes(status_code=status,parity_code=parity_code,send_rounds=send_rounds,total_frames=total_frames)  #默认发送所有帧
                                    # for control_frame_img in control_frame_imgs:
                                    #     control_frame_img_send_queue.put(control_frame_img)
                                    assert len(control_frame_imgs)==1
                                    self.showImg(control_frame_imgs[0])
                                    parity_code^=1  #
                                    send_control_frame_flag=True  #我先发
                                    status=2  #直接进入数据发送阶段
                                    print(f'status: {status}')
                                    t1=time.time()
                                    time_start=time.time()
                                else:
                                    print(f'detect status_code:{control_frame_dict["status_code"]} from sender but expected status_code 0')


                elif status==1:  #准备阶段
                    if(control_frame_img_send_queue.empty()): #如果所有控制帧都已经发送，那么直接进入阶段2
                        status=2
                        print(f'status: {status}')
                        t1=time.time()
                        # time_start=time.time()
                    else:
                        
                        qrcode_data=decoder.QRCode_decode(img0)
                        if(qrcode_data!=None):
                            control_frame_dict=decoder.decode_control_frame(qrcode_data)
                            if(control_frame_dict!=None):
                                print(f'receive control_frame:{control_frame_dict}')


                                if(control_frame_dict['parity_code']!=sender_parity_code):
                                    continue
                                else:
                                    sender_parity_code^=1
                                if(control_frame_dict['status_code']==1):
                                    # total_frames=control_frame_dict['total_frames']
                                    # qrcode_type=control_frame_dict['qrcode_type']
                                    # use_compress=control_frame_dict['use_compress']
                                    # send_parity_code=control_frame_dict['parity_code']
                                    send_control_frame_flag=True  #可以继续发送下一帧控制图像

                                    if(control_frame_img_send_queue.qsize()==1):
                                        print('status 2')
                                        status=2
                                        t1=time.time()


                        

                elif status==2:

                    all_cnt+=1
                    CQRCode_data=decoder.CQRCode_decode(img0,qrcode_type=qrcode_type)


                    if(CQRCode_data!=None ):
                        if not save_flag:
                            save_img(img0)
                            save_flag=True
                        data_frame=decoder.decode_data_frame(CQRCode_data)
                        if(data_frame!=None):
                            if last_frame_cnt==data_frame['seq_num']:
                                continue
                            if data_frame['seq_num'] not in decoded_frame_dict:
                                decoded_frame_dict[data_frame['seq_num']]=data_frame
                                print(f'new detect:{data_frame["seq_num"]}')
                                t1=time.time()
                            if data_frame['seq_num']==end_frame_num:
                                send_rounds+=1
                                if(len(decoded_frame_dict.keys())==total_frames):
                                    print('status 3')
                                    status=3
                                    t1=time.time()
                                    control_frame_imgs=encoder.generate_control_qrcodes(status_code=status,parity_code=parity_code,send_rounds=send_rounds,total_frames=total_frames,decoded_frame_dict=decoded_frame_dict)
                                    assert(len(control_frame_imgs)==1)
                                    self.showImg(control_frame_imgs[0])
                                    parity_code^=1

                                else:


                                    print(f'have received: {decoded_frame_dict.keys()}')

                                    print('status 1')
                                    status=1

                                    end_frame_num=get_last_seq_num(decoded_frame_dict,total_frames)
                                    control_frame_imgs=encoder.generate_control_qrcodes(status_code=status,parity_code=parity_code,send_rounds=send_rounds,total_frames=total_frames,decoded_frame_dict=decoded_frame_dict)
                                    for control_frame_img in control_frame_imgs:
                                        control_frame_img_send_queue.put(control_frame_img)
                                    send_control_frame_flag=True  #我先发
                                    
                                    t1=time.time()
                            
                            last_frame_cnt=data_frame['seq_num']
                            
                        # else:

                            # 这个要算进 
                            # print(f'receive data {CQRCode_data} but not able to decode as dataframe ?这个还没算进err_cnt !')
                    else:
                        err_cnt+=1
                elif status==3:
                    # ids=detector.identify(img0)
                    qrcode_data=decoder.QRCode_decode(img0)
                    if(qrcode_data!=None):
                        control_frame_dict=decoder.decode_control_frame(qrcode_data)
                        if(control_frame_dict!=None):
                            print(f'receive control_frame:{control_frame_dict}')

                            if(control_frame_dict['parity_code']!=sender_parity_code):
                                continue
                            else:
                                sender_parity_code^=1
                            if(control_frame_dict['status_code']==3):
                                status=4
                                print('进入Status 4')
                                control_frame_imgs=encoder.generate_control_qrcodes(status_code=status,parity_code=parity_code)
                                assert(len(control_frame_imgs)==1)
                                
                                self.showImg(control_frame_imgs[0])
                                parity_code^=1
                                t1=time.time()
                                time_end=time.time()
                                cv2.waitKey(WAIT_TO_END_TIME)


                    
                else:
                    print('status 4')
                    loop_flag=False
                    cv2.destroyAllWindows()
                    result_dict={}
                    print(f'err_cnt:{err_cnt}')
                    result_dict['err_cnt']=err_cnt
                    print(f'all_cnt:{all_cnt}')
                    result_dict['all_cnt']=all_cnt
                    print(f'detect_accur:{err_cnt/all_cnt*1.0}')
                    result_dict['detect_accur']=err_cnt/all_cnt*1.0
                    print(f'transmission_time:{time_end-time_start}')
                    result_dict['transmission_time']=time_end-time_start
                    print(f'send_rounds:{send_rounds}')
                    result_dict['send_rounds']=send_rounds
                    
                    data=decoder.reassemble_data_frames(decoded_frame_dict,use_compress=use_compress,total_frames_expected=total_frames)


                    print(f'speed:{len(data)/(time_end-time_start)*1.0} byte/s')
                    result_dict['speed']=len(data)/(time_end-time_start)*1.0

                    result_dict['qrcode_type']=qrcode_type
                    result_dict['use_compress']=use_compress
                    log_experiment_result(result_dict)

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
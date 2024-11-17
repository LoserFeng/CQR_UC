import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
from cv2.wechat_qrcode import WeChatQRCode
import math
import qrcode
from bitstring import BitStream,BitArray,Bits
from PIL import Image
import base64
import zlib


class Decoder:
    def __init__(self,test=False) -> None:
        self.detector = WeChatQRCode(detector_prototxt_path="qr_mode/detect.prototxt", detector_caffe_model_path="qr_mode/detect.caffemodel",super_resolution_prototxt_path="qr_mode/sr.prototxt", super_resolution_caffe_model_path="qr_mode/sr.caffemodel")
        #设置初始门限值 ，自己按照需求更新一下
        #清水
        self.red_threshold=140
        self.green_threshold=180
        self.blue_threshold=200  

        self.test=test
        if(test):
        #    cv2.namedWindow('test',cv2.WINDOW_GUI_NORMAL)
           cv2.namedWindow('R_view',cv2.WINDOW_GUI_NORMAL)
           cv2.namedWindow('G_view',cv2.WINDOW_GUI_NORMAL)
           cv2.namedWindow('B_view',cv2.WINDOW_GUI_NORMAL)




        self.blue_err_cnt=0
        self.red_err_cnt=0
        self.green_err_cnt=0
        self.try_float_arr=[0,-10,20,-30,40,-50,60,-70,80,-40]  # 0 -10 10 -20 20 -30 30 -40 40
        self.max_err_times=10

        self._control_frame_type=9   #0b 1001
        self._data_frame_type=10   # 0b 1002
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
        data_list, points = self.detector.detectAndDecode(img)
        # print(points)
        # print(f'data_list:{data_list}')
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
    




    def ProcessCQRCode_R(self,img,super:bool=False):
        if super:
            if self.red_err_cnt>=self.max_err_times:
                self.red_threshold+=self.try_float_arr[(self.red_err_cnt-self.max_err_times)%len(self.try_float_arr)]
            img[img[:,:,2]>=self.red_threshold]=255
            img[img[:,:,2]<self.red_threshold]=0
        img[:,:,0]=img[:,:,2]
        img[:,:,1]=img[:,:,2]


        #cv2.imshow('img_1',img)

        img_R=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # if bilateralFilter:
        #     img_R=cv2.bilateralFilter(img_R,  7, 150, 10)
       # ret,img_G=cv2.threshold(img_G,180, 255,cv2.THRESH_BINARY)
        #img_G=cv2.equalizeHist(img_G)


        return img_R



    

    def ProcessCQRCode_G(self,img,super:bool=False):
        if super:
            if self.green_err_cnt>=self.max_err_times:
                self.green_threshold+=self.try_float_arr[(self.green_err_cnt-self.max_err_times)%len(self.try_float_arr)]
            img[img[:,:,1]>=self.green_threshold]=255
            img[img[:,:,1]<self.green_threshold]=0
        img[:,:,0]=img[:,:,1]
        img[:,:,2]=img[:,:,1]

        #cv2.imshow('img_G',img)
        img_G=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # if bilateralFilter:
        #     img_G=cv2.bilateralFilter(img_G,  7, 150, 10)



       # ret,img_G=cv2.threshold(img_G,180, 255,cv2.THRESH_BINARY)
        #img_G=cv2.equalizeHist(img_G)


        return img_G





 
    def ProcessCQRCode_B(self,img,super:bool=False):
        if super:
            if self.blue_err_cnt>=self.max_err_times:
                self.blue_threshold+=self.try_float_arr[(self.blue_err_cnt-self.max_err_times)%len(self.try_float_arr)]
            img[img[:,:,0]>=self.blue_threshold]=255
            img[img[:,:,0]<self.blue_threshold]=0
        img[:,:,1]=img[:,:,0]
        img[:,:,2]=img[:,:,0]

        #cv2.imshow('img_G',img)
        img_B=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)




       # ret,img_G=cv2.threshold(img_G,180, 255,cv2.THRESH_BINARY)
        #img_G=cv2.equalizeHist(img_G)


        return img_B






    def get_color_list(self,qrcode_type):  #qrcode_type的顺序是倒叙，所以应该是011是 red green
        color_list=[]
        num_colors=0
        colors=['red','green','blue']
        for i in range(4):  #暂时只有3个通道
            if((1<<i)&qrcode_type!=0):
                color_list.append(1)
                num_colors+=1
            else:
                color_list.append(0)

        assert num_colors<=3

        return color_list
        


    def CQRCode_decode(self,img,qrcode_type:int,test:bool=False,super:bool=False):  # super表示是否需要自调整颜色阀域
        colors=[]

        color_list=self.get_color_list(qrcode_type)
        if(color_list[3]==1):  #
            cv2.imshow('R_view',img)
            return self.QRCode_decode(img)
        R_data=None
        G_data=None
        B_data=None
        img_R=None
        img_B=None
        img_G=None
        res:bytes=''
        if color_list[0]:
            img_R=self.ProcessCQRCode_R(img.copy(),super)
            R_data =self.QRCode_decode(img_R)
            if R_data ==None:
                self.red_err_cnt+=1
            else:
                self.red_err_cnt=0


            if R_data!=None and res!=None:
                res+=R_data
            else:
                res=None
                # return None
            
        if color_list[1]:
            img_G=self.ProcessCQRCode_G(img.copy(),super)
            G_data =self.QRCode_decode(img_G)
            if G_data ==None:
                self.green_err_cnt+=1
            else:
                self.green_err_cnt=0


            if G_data!=None and res!=None:
                res+=G_data
            else:
                res=None



        if color_list[2]:
            img_B=self.ProcessCQRCode_B(img.copy(),super)
            B_data =self.QRCode_decode(img_B)
            if B_data ==None:
                self.blue_err_cnt+=1
            else:
                self.blue_err_cnt=0
        

            if B_data!=None and res!=None:
                res+=B_data
            else:
                res=None


        
        if super:
            print("red_threshold:",self.red_threshold)
            print("green_threshold:",self.green_threshold)
            print("blue_threshold:",self.blue_threshold)

        # res=None
        # if(R_data!=None and G_data!=None and B_data!=None):
        #     res=R_data+G_data+B_data
        # if( R_data!=None):
        #     print('R:',R_data)
        # if( G_data!=None):
        #     print('G:',G_data)
        # if( B_data!=None):
        #     print('B:',B_data)
        if(self.test):
            if(img_R is not None):
                cv2.imshow('R_view',img_R)
            if(img_G is not None):
                cv2.imshow('G_view',img_G)
            if(img_B is not None):
                cv2.imshow('B_view',img_B)
        if test:
            return img_R,img_G,img_B,res
        else:
            return res



    def decode_lack_num(self,lack_num):  #计算编号
        res=0
        lack_num_list=[]
        idx=0
        while(lack_num!=0):
            if(lack_num&1):
                lack_num_list.append(idx)
            lack_num>>=1
            idx+=1



        return lack_num_list


    



    def decode_control_frame(self,control_frame):
        frame_type=0
        status_code=0
        total_frames=0
        lack_num=0

        # bs.append(f'0b{frame_type:04b}')      # 4 位
        # bs.append(f'0b{qrcode_type:04b}')      # 4 位
        # bs.append(f'0b{status_code:04b}')      # 4 位
        
        # bs.append(f'0b{use_compress:01b}')       # 16 位
        # bs.append(f'0b{total_frames:01b}')
        # bs.append(f'0b{seq_num:0127b}')     # 8 位

        
        control_frame=base64.a85decode(control_frame)


        # 创建 BitStream 对象
        bs = BitStream(bytes=control_frame)
        
        # 读取字段
        frame_type = bs.read('uint:4')    # 14位
        if(frame_type !=self._control_frame_type):
            print(f'Invalid frame type(Not control frame): {frame_type} expected {self._control_frame_type}')
            return None
        qrcode_type = bs.read('uint:4')  
        status_code = bs.read('uint:4')    # 2位
        

        use_compress=bs.read('uint:1')
        total_frames = bs.read('uint:19')      # 16位
        seq_num = bs.read('uint:32')
        # # 读取 variable_data
        # variable_data_bits = bs.read(f'bytes:{total_frames}')

        
        return {
            'frame_type': frame_type,
            'qrcode_type': qrcode_type,
            'status_code': status_code,
            'use_compress':use_compress,
            'total_frames': total_frames,
            'seq_num': seq_num,

        }


    def decode_data_frame(self,data_frame):
        """
        解码数据帧，提取 frame_type, seq_num, datasize, variable_data
        :param data_frame: bytes，数据帧
        :return: dict，包含各个字段
        """
        data_frame=base64.a85decode(data_frame)

        
        # 创建 BitStream 对象
        bs = BitStream(bytes=data_frame)
        
        # 读取字段
        frame_type = bs.read('uint:4')      # 8 位
        if(frame_type !=self._data_frame_type):
            return None
        qrcode_type = bs.read('uint:4')      # 8 位
        # use_compress = bs.read('uint:1')         # 1 位
        seq_num = bs.read('uint:32')         # 8 位
        datasize = bs.read('uint:16')       # 16 位
        variable_data = bs.read(f'bytes:{datasize}')  # 可变长度数据
        

        # if use_compress:  #合并后再解压
        #     variable_data=zlib.decompress(variable_data)



        return {
            'frame_type': frame_type,
            'qrcode_type':qrcode_type,
            # 'use_compress':use_compress,
            'seq_num': seq_num,
            'datasize': datasize,
            'variable_data': variable_data
        }


    def reassemble_data_frames(self,decoded_frame_dict,use_compress=False,total_frames_expected=0):
        """
        重组多个数据帧，恢复原始数据。

        
        :param data_frames: list of bytes，多个数据帧
        :return: str，重组后的原始数据
        """
        # decoded_frame_dict = []
        # total_frames_expected = None
        
        # for data_frame in data_frames:
        #     # decoded = self.decode_data_frame(frame)
            
        #     # 确定总帧数
        #     # if total_frames_expected is None:
        #     #     total_frames_expected = ['total_frames']
        #     # elif total_frames_expected != decoded['total_frames']:
        #     #     raise ValueError("数据帧的总帧数不一致")
            
        #     decoded_frame_dict.append(self.decode_data_frame(data_frame))
        
        # 验证是否收到了所有帧
        if len(decoded_frame_dict) != total_frames_expected:
            raise ValueError(f"期望 {total_frames_expected} 个数据帧，但收到 {len(decoded_frame_dict)} 个")
        
        # use_compress=decoded_frame_dict[0]['use_compress']

        # 按序列号排序
        # decoded_frame_dict.sort(key=lambda x: x['seq_num'])
        
        # 拼接 variable_data
        original_data_bytes = b''.join(decoded_frame_dict[idx]['variable_data'] for idx in range(len(decoded_frame_dict.keys())))
        
        if use_compress:
            original_data_bytes=zlib.decompress(original_data_bytes)

        # 解码为字符串
        original_data = original_data_bytes.decode('utf-8')
        
        return original_data






class Encoder:  #Encoder 已经完成
    
    def __init__(self,version:int,qrcode_type:int,error_correct_level:str='L',use_compress=False):
        self._capacity_table=np.load('qrcode_capacity_table.npy',allow_pickle=True).item()
        self._version=version
        self._error_correct_level=error_correct_level
        self._error_correct_level_dict={
        'H': qrcode.constants.ERROR_CORRECT_H,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'L': qrcode.constants.ERROR_CORRECT_L
        }
        # self._color_channel_num=color_channel_num
        self._qrcode_type=qrcode_type
        self._control_frame_type=9   #0b 1001
        self._data_frame_type=10   # 0b 1002
        self._use_compress=use_compress




        
    


    
    def generate_qrcode(self,data, filename=None,version:int=None,error_correct_level:str=None,back_color='white',border=1):  #返回  h w 3 类型的 numpy
        qr = qrcode.QRCode(
            version=self._version if version==None else version, # 1 是21*21的版本
            error_correction=self._error_correct_level_dict[self._error_correct_level if error_correct_level==None else error_correct_level],
            box_size=10,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
    
        img = qr.make_image(fill='black', back_color=back_color)
        # img=img.resize((1000,1000),Image.NEAREST)

        numpy_image = np.array(img)
        if len(numpy_image.shape) == 3:  # Check if it's a color image
            numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
        if len(numpy_image.shape) == 2:  # Grayscale image (2D array)
            numpy_image_uint8 = (numpy_image * 255).astype(np.uint8)
            numpy_image = cv2.cvtColor(numpy_image_uint8, cv2.COLOR_GRAY2BGR)  # Convert to 3-channel BGR
        if filename is not None:
            img.save(filename)
        return numpy_image
    

        # img.save(filename)
        # img=cv2.imread(filename)
        # cv2.imshow('Image',img)
        # cv2.waitKey(0)








    def get_lack_num(self,total_frames,decoded_frame_dict):  #根据缺少的图片的序号计算一个int类型的不同序号的和
        res=0
        
        for i in range(total_frames):
            if i not in decoded_frame_dict:
                res|=(1<<i)
        return res


    



    def get_color_list(self,qrcode_type):  #qrcode_type的顺序是倒叙，所以应该是011是 red green
        color_list=[]
        num_colors=0

        for i in range(4):  #暂时只有3个通道
            if((1<<i)&qrcode_type!=0):
                color_list.append(1)
                num_colors+=1
            else:
                color_list.append(0)

        assert num_colors<=3

        return color_list



 
    def generate_control_qrcode(self,status_code,total_frames=0,seq_num=0,):
        frame_type=self._control_frame_type
        qrcode_type=self._qrcode_type
        use_compress=self._use_compress
        lack_num=0

        control_frame=self.generate_control_frame(frame_type,qrcode_type,status_code,use_compress,total_frames,seq_num)
        
        qrcode_img=self.generate_qrcode(control_frame,version=1,error_correct_level='H')  #version=1表示越小越好

        return qrcode_img


    def make_cqrcode(self,data,error_correct_level:str,color_list,filename=None):
        # if(qrcode_type==None):
        #     qrcode_type=self._qrcode_type
        colors=[(255,0,0), (0,255,0), (0,0,255),(255,255,255)]
        colors=[colors[i] for i in range(len(colors)) if color_list[i]!=0]
        num_colors=sum(color_list)
        cqrcode_img=None
        qrcode_imgs=[]
        if(num_colors==0):
            qrcode_imgs.append(self.generate_qrcode(data))
        else:
            
            
            # assert num_colors!=1   #这样子依然是单色的二维码
            part_size=(len(data)+(num_colors-1))//(num_colors)
            data_splits=[data[i*part_size:(i+1)*part_size] for i in range(num_colors)]
            for i,data_split in enumerate(data_splits):
                qrcode_imgs.append(self.generate_qrcode(data=data_split,filename=None,back_color=colors[i]))
            
        assert len(qrcode_imgs)!=0

        cqrcode_img=np.zeros((qrcode_imgs[0].shape[0],qrcode_imgs[0].shape[1],3),dtype=np.uint8)

        for img in qrcode_imgs:
            cqrcode_img=cqrcode_img+img
        


        return cqrcode_img
        
        
        


        



        



    def generate_data_cqrcodes(self,data, error_correct_level:str=None,qrcode_type:int=None):

        img=None
        cqrcode_imgs=[]
        data_bytes=data.encode('utf-8')
        total_size=len(data_bytes) #52
        max_part_size=self._capacity_table[self._version][self._error_correct_level]  #17
        color_list=self.get_color_list(self._qrcode_type)

        num_colors=sum(color_list) 
        max_part_size*=num_colors
        max_part_size-=5  #因为封装帧的头部需要大概4字节？  
        max_part_size=int(max_part_size/1.25)  #由于a85编码的问题1.25的编码效率  TO TEST




        data_bytes_splits=self.split_data_bytes(data_bytes,max_part_size,self._use_compress)
        for seq_num,data_bytes_split in enumerate(data_bytes_splits):
            #对数据进行封装->data_frame

            
            data_frame=self.generate_data_frame(self._data_frame_type,self._qrcode_type,seq_num,len(data_bytes_split),data_bytes_split)

            cqrcode_img=self.make_cqrcode(data=data_frame,error_correct_level=self._error_correct_level,color_list=color_list)
            # self.generate_qrcode(data_frame,error_correct_level=self._error_correct_level,data)
            cqrcode_imgs.append(cqrcode_img)

        # if filename is not None:
        #     img.save(filename)

        return cqrcode_imgs


    


    def split_data_bytes(self,data_bytes, max_part_size,use_compress=0):
        """
        将字节数据拆分为多个部分，每部分不超过 max_part_size 字节。
        
        :param data_bytes: bytes，原始数据
        :param max_part_size: int，每部分的最大字节数
        :return: list of bytes，拆分后的数据部分
        """
        parts = []
        if(use_compress):  #先压缩，再分组
            data_bytes=zlib.compress(data_bytes)
        # data_bytes=base64.a85encode(data_bytes)


        total_length = len(data_bytes)  #300
        for i in range(0, total_length, max_part_size):
            parts.append(data_bytes[i:i + max_part_size])
        return parts




    def generate_control_frame(self,frame_type,qrcode_type,status_code=2,use_compress=False,total_frames=0,seq_num=0):  #status_code 0表示准备就绪 1表示继续传输 2表示结束
        res=0
        # status_code=2  #2位 ？
        frame_type_length=4
        qrcode_type_length=4
        status_code_length=4
        
        use_compress_length=1
        total_frames_length=19  #用帧的数量表示
        seq_num_length=32

        if not (0 <= frame_type < (1 << frame_type_length)):
            raise ValueError("frame_type 超出范围 (0-15)")
        
        if not (0 <= qrcode_type < (1 << qrcode_type_length)):
            raise ValueError("qrcode_type 超出范围 (0-15)")
        if not (0 <= status_code < (1 << status_code_length)):
            raise ValueError("status_code 超出范围 (0-15)")
        
        if not (0 <= use_compress < (1 << use_compress_length)):
            raise ValueError("use_compress 超出范围 (0-1)")
        if not (0 <= total_frames < (1 << total_frames_length)):
            raise ValueError("total_frames 超出范围 ")
        if not (0 <= seq_num_length < (1 << seq_num_length)):
            raise ValueError("seq_num_length 超出范围 (0-2^128-1)")


        bs = BitStream()
        bs.append(f'0b{frame_type:04b}')      # 4 位
        bs.append(f'0b{qrcode_type:04b}')      # 4 位
        bs.append(f'0b{status_code:04b}')      # 4 位
        
        bs.append(f'0b{use_compress:01b}')       # 16 位
        bs.append(f'0b{total_frames:01b}')
        bs.append(f'0b{seq_num:032b}')     # 8 位
        # bs.append(f'0b{lack_num:0128b}')      # 128 位
        

        
        # 转换为字节
        control_frame = bs.tobytes() 
        print(f'control_frame:{control_frame}')


        control_frame=base64.a85encode(control_frame)




        # qrcode_img=self.qrcode_generator(res)
        

        return control_frame  #把数据帧返回一下





        

    def generate_data_frame(self,frame_type,qrcode_type,seq_num,datasize,variable_data):
        frame_type_length=4
        qrcode_type_length=4

        seq_num_length=32
        datasize_length=16  #用字节表示？
        variable_data_length=0

        # variable_data=base64.a85decode(variable_data)  #传输的数据是未被进行任何压缩编码的
        # if(use_compress):  #由于之前计算的时候是先压缩的，所以先解压
        #     variable_data=zlib.decompress(variable_data)

            

        
        if not (0 <= frame_type < (1 << frame_type_length)):
            raise ValueError(f"frame_type 超出范围 (0-{(1 << frame_type_length) - 1})")
        
        if not (0 <= qrcode_type < (1 << qrcode_type_length)):
            raise ValueError(f"qrcode_type 超出范围 (0-{(1 << qrcode_type_length) - 1})")
        
        # if not (0<=use_compress<(1 << use_compress)):
        #     raise ValueError(f"use_compress 超出范围 (0-{(1 << use_compress_length) - 1})")

        if not (0 <= seq_num < (1 << seq_num_length)):
            raise ValueError(f"seq_num 超出范围 (0-{(1 << seq_num_length) - 1})")
        

        if not (0 <= datasize < (1 << datasize_length)):
            raise ValueError(f"datasize 超出范围 (0-{(1 << datasize_length) - 1})")
        if len(variable_data) != datasize:
            raise ValueError("variable_data 的长度与 datasize 不一致")
        
        # if(use_compress):
        #     data_frame=zlib.compress(data_frame)   #对于简短的数据，反而会增加它的长度，对于长的数据，才有比较好的压缩比


        # 创建 BitStream 对象
        bs = BitStream()
        bs.append(f'0b{frame_type:04b}')      # 4 位
        bs.append(f'0b{qrcode_type:04b}')      # 4 位
        # bs.append(f'0b{use_compress:01b}')        # 1 位
        bs.append(f'0b{seq_num:032b}')        # 8 位
        bs.append(f'0b{datasize:016b}')      # 16 位
        bs.append(Bits(bytes=variable_data))  # 可变长度数据
        
        # 转换为字节
        data_frame = bs.tobytes()  #19 +4 23
        
        data_frame=base64.a85encode(data_frame)  #最后对数据再次进行编码？
        # data_frame.decode('utf8')
        # data_frame=base64.b85decode(data_frame)
        # zlib.decompress(data_frame)
        
        
        return data_frame



        

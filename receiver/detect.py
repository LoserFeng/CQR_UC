

import cv2
import re
import numpy as np

import onnxruntime as ort

from utils import plot_one_box,_make_grid,cal_outputs,post_process_opencv,infer_img


class Detector:
    def __init__(self) -> None:
        model_pb_path = "./weights/flag_detect.onnx"
        so = ort.SessionOptions()
        self.net = ort.InferenceSession(model_pb_path, so)
        
        # 标签字典
        self.dic_labels= {0:'ready_flag',
                1:'reading_flag'}
        
        # 模型参数
        self.model_h = 320
        self.model_w = 320
        self.nl = 3
        self.na = 3
        self.stride=[8.,16.,32.]
        anchors = [[10, 13, 16, 30, 33, 23], [30, 61, 62, 45, 59, 119], [116, 90, 156, 198, 373, 326]]
        self.anchor_grid = np.asarray(anchors, dtype=np.float32).reshape(self.nl, -1, 2)
        pass




    def identify(self,img):
        det_boxes,scores,ids = infer_img(img,self.net,self.model_h,self.model_w,self.nl,self.na,self.stride,self.anchor_grid,thred_nms=0.4,thred_cond=0.5)
        return ids
    
    def get_boxs(self,img):
        det_boxes,scores,ids = infer_img(img,self.net,self.model_h,self.model_w,self.nl,self.na,self.stride,self.anchor_grid,thred_nms=0.4,thred_cond=0.5)
        return det_boxes
    
import cv2
import numpy as np
import onnxruntime as ort
import time
import random
from bitstring import BitStream,BitArray, Bits




def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    """
    description: Plots one bounding box on image img,
                 this function comes from YoLov5 project.
    param: 
        x:      a box likes [x1,y1,x2,y2]
        img:    a opencv image object
        color:  color to draw rectangle, such as (0,255,0)
        label:  str
        line_thickness: int
    return:
        no return
    """
    tl = (
        line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
    )  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(
            img,
            label,
            (c1[0], c1[1] - 2),
            0,
            tl / 3,
            [225, 255, 255],
            thickness=tf,
            lineType=cv2.LINE_AA,
        )

def _make_grid( nx, ny):
        xv, yv = np.meshgrid(np.arange(ny), np.arange(nx))
        return np.stack((xv, yv), 2).reshape((-1, 2)).astype(np.float32)

def cal_outputs(outs,nl,na,model_w,model_h,anchor_grid,stride):
    
    row_ind = 0
    grid = [np.zeros(1)] * nl
    for i in range(nl):
        h, w = int(model_w/ stride[i]), int(model_h / stride[i])
        length = int(na * h * w)
        if grid[i].shape[2:4] != (h, w):
            grid[i] = _make_grid(w, h)

        outs[row_ind:row_ind + length, 0:2] = (outs[row_ind:row_ind + length, 0:2] * 2. - 0.5 + np.tile(
            grid[i], (na, 1))) * int(stride[i])
        outs[row_ind:row_ind + length, 2:4] = (outs[row_ind:row_ind + length, 2:4] * 2) ** 2 * np.repeat(
            anchor_grid[i], h * w, axis=0)
        row_ind += length
    return outs



def post_process_opencv(outputs,model_h,model_w,img_h,img_w,thred_nms,thred_cond):
    conf = outputs[:,4].tolist()
    c_x = outputs[:,0]/model_w*img_w
    c_y = outputs[:,1]/model_h*img_h
    w  = outputs[:,2]/model_w*img_w
    h  = outputs[:,3]/model_h*img_h
    p_cls = outputs[:,5:]
    if len(p_cls.shape)==1:
        p_cls = np.expand_dims(p_cls,1)
    cls_id = np.argmax(p_cls,axis=1)

    p_x1 = np.expand_dims(c_x-w/2,-1)
    p_y1 = np.expand_dims(c_y-h/2,-1)
    p_x2 = np.expand_dims(c_x+w/2,-1)
    p_y2 = np.expand_dims(c_y+h/2,-1)
    areas = np.concatenate((p_x1,p_y1,p_x2,p_y2),axis=-1)
    
    areas = areas.tolist()
    ids = cv2.dnn.NMSBoxes(areas,conf,thred_cond,thred_nms)
    if len(ids)>0:
        return  np.array(areas)[ids],np.array(conf)[ids],cls_id[ids]
    else:
        return [],[],[]
def infer_img(img0,net,model_h,model_w,nl,na,stride,anchor_grid,thred_nms=0.4,thred_cond=0.5):
    # 图像预处理
    img = cv2.resize(img0, [model_w,model_h], interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    blob = np.expand_dims(np.transpose(img, (2, 0, 1)), axis=0)

    # 模型推理
    outs = net.run(None, {net.get_inputs()[0].name: blob})[0].squeeze(axis=0)

    # 输出坐标矫正
    outs = cal_outputs(outs,nl,na,model_w,model_h,anchor_grid,stride)

    # 检测框计算
    img_h,img_w,_ = np.shape(img0)
    boxes,confs,ids = post_process_opencv(outs,model_h,model_w,img_h,img_w,thred_nms,thred_cond)

    return  boxes,confs,ids




    
    
    






def get_lack_num(data_list,received_list):  #根据缺少的图片的序号计算一个int类型的不同序号的和
    res=0
    for i in range(len(data_list)):
        if i not in received_list:
            res|=(1<<i)
    return res









    




def split_bytes(data_bytes, n):  #废物
    """
    将字节数据拆分为 n 个部分，尽可能均匀分配。
    
    :param data_bytes: bytes，原始数据
    :param n: int，拆分的部分数
    :return: list of bytes，拆分后的数据部分
    """
    if n <= 0:
        raise ValueError("n 必须是正整数")
    
    length = len(data_bytes)
    part_size = length // n
    remainder = length % n
    
    parts = []
    start = 0
    for i in range(n):
        # 分配余数
        end = start + part_size + (1 if i < remainder else 0)
        parts.append(data_bytes[start:end])
        start = end
    
    return parts





def add_white_frame(square_image,occupy_image_width=720,occupy_image_height=720,screen_width=1720,screen_height=1080):
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





def get_last_seq_num(decoded_frame_dict,total_frames):
    end_frame_num=total_frames-1
    for i in range(total_frames):
        if i not in decoded_frame_dict:
            end_frame_num=i
    return end_frame_num


import datetime

def log_experiment_result(result):
    # 获取当前时间并格式化为字符串
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 将结果格式化为日志信息
    log_entry = f"{timestamp} - {result}\n"
    
    # 打开（或创建）日志文件并追加写入
    with open("./logs/experiment_log.txt", "a") as log_file:
        log_file.write(log_entry)

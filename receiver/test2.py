from bitstring import BitStream, Bits
import qrcode
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def generate_qr(data_frame, qr_filename='qrcode.png'):
    """
    生成包含字节数据的二维码。

    参数：
    - data_frame: bytes 类型的字节数据
    - qr_filename: 生成的二维码图像文件名

    返回：
    - PIL.Image 对象的二维码图像
    """
    qr = qrcode.QRCode(
        version=None,  # 自动选择适当的版本
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高纠错级别
        box_size=10,  # 每个模块的像素大小
        border=4,  # 边框宽度（以模块数表示）
    )
    
    qr.add_data(data_frame)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white').convert("RGB")
    img.save(qr_filename)
    img.show()
    return img

def split_bytes(data_frame):
    """
    将字节数据拆分为两部分。

    参数：
    - data_frame: bytes 类型的字节数据

    返回：
    - part1: 字节数据的前半部分
    - part2: 字节数据的后半部分
    """
    split_size = len(data_frame) // 2
    part1 = data_frame[:split_size]
    part2 = data_frame[split_size:]
    return part1, part2

def main():
    # 示例：构建 BitStream 数据
    frame_type = 1
    qrcode_type = 2
    seq_num = 5
    datasize = 12
    variable_data = b'Hello, this is variable data!'  # 示例的字节数据

    # 创建 BitStream 实例
    bs = BitStream()
    bs.append(f'0b{frame_type:04b}')          # 4 位
    bs.append(f'0b{qrcode_type:04b}')        # 4 位
    bs.append(f'0b{seq_num:08b}')           # 8 位
    bs.append(f'0b{datasize:016b}')         # 16 位
    bs.append(Bits(bytes=variable_data))     # 可变长度数据

    # 转换为字节
    data_frame = bs.tobytes()
    print("原始字节数据长度:", len(data_frame))
    print("原始字节数据:", data_frame)

    # 拆分字节数据
    part1, part2 = split_bytes(data_frame)
    print("部分1字节数据长度:", len(part1))
    print("部分1字节数据:", part1)
    print("部分2字节数据长度:", len(part2))
    print("部分2字节数据:", part2)

    # 生成二维码
    qr_img1 = generate_qr(part1, qr_filename='qrcode_part1.png')
    qr_img2 = generate_qr(part2, qr_filename='qrcode_part2.png')

if __name__ == "__main__":
    main()
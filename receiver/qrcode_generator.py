
from PIL import Image
import qrcode
import cv2
import numpy as np



# cv2.namedWindow('Image')


class QRCodeGenerator:
    _error_correct_level_dict={
        'H': qrcode.constants.ERROR_CORRECT_H,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'L': qrcode.constants.ERROR_CORRECT_L
    }
    
    

    def generate_qrcode(self,data, filename=None,error_correct_level:str='M',back_color='white'):  #返回  h w 3 类型的 numpy
        qr = qrcode.QRCode(
            version=1, # 1 是21*21的版本
            error_correction=self._error_correct_level_dict[error_correct_level],
            box_size=10,
            border=3,
        )
        qr.add_data(data)
        qr.make(fit=True)
    
        img = qr.make_image(fill='black', back_color=back_color)

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


    def generate_cqrcode(self,data, filename=None,error_correct_level:str='M',channel_num=2):

        data//channel_num
        
        self.generate_qrcode()


        if filename is not None:
            img.save(filename)


 
# # 使用函数生成二维码
# data='1'*3000
# generate_qrcode(data, 'hello_world.png')




if __name__ == '__main__':
    generator=QRCodeGenerator()
    img=generator.generate_qrcode('12312312',)
    cv2.namedWindow('Test')
    cv2.imshow('Test',img)
    cv2.waitKey(0)
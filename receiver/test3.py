from CQRCode import Encoder,Decoder
import cv2
import os

encoder=Encoder(1,3)  #version qrcode_type
# decoder=Decoder(test=True)
root_dir='C:/Users/surface/Desktop/CQRCodes'


# cqrcodes=encoder.generate_data_cqrcodes('sdajdisojiasd')

# for cqrcode in cqrcodes:
#     CQRCode_data=decoder.CQRCode_decode(cqrcode,qrcode_type=3)
#     print(CQRCode_data)
#     test=decoder.decode_data_frame(CQRCode_data)
#     print(test)

in_str='ansdjasopsdioajdiosajdiojsaiodjsaoidjoisajdoisdiajidjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjsidajdsisjadiojsaiodjioasjdiojaiosjdiosjad'
# in_str=in_str.encode('utf-8')
# test_data=encoder.generate_data_frame(3,2,len(in_str),in_str)

for version in range(1,15):
    for qrcode_type in range(1,9):
        encoder=Encoder(version,qrcode_type)
        test_qrcodes=encoder.generate_data_cqrcodes(in_str)
        cv2.imwrite(os.path.join(root_dir,f'{version}_{qrcode_type}.jpg'),test_qrcodes[0])



# decoded_frame_dict={}
# for qrcode in test_qrcodes:
    # out_str=decoder.CQRCode_decode(qrcode,qrcode_type=3)
    # frame_dict=decoder.decode_data_frame(out_str)
    # decoded_frame_dict[frame_dict['seq_num']]=frame_dict


# result=decoder.reassemble_data_frames(decoded_frame_dict,total_frames_expected=6)

# print(result)


# out_str

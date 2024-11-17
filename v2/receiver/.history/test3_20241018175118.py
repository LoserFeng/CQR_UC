from CQRCode import Encoder,Decoder


encoder=Encoder(8,8)
decoder=Decoder(test=True)



# cqrcodes=encoder.generate_data_cqrcodes('sdajdisojiasd')

# for cqrcode in cqrcodes:
#     CQRCode_data=decoder.CQRCode_decode(cqrcode,qrcode_type=3)
#     print(CQRCode_data)
#     test=decoder.decode_data_frame(CQRCode_data)
#     print(test)

in_str='ansdjasopsdioajdiosajdiojsaiodjsaoidjoisajdoisdiajidjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjsidajdsisjadiojsaiodjioasjdiojaiosjdiosjad'
in_str=in_str.encode('utf-8')
test_data=encoder.generate_data_frame(3,2,len(in_str),in_str)

out_str=decoder.decode_data_frame(test_data)

print(out_str)

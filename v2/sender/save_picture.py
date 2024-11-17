import cv2

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

for i in range(100):
    # 拍照
    ret, frame = cap.read()


    # 如果拍照成功
    if ret and i==100:
        # 保存图片
        cv2.imwrite('photo.jpg', frame)
        print("照片已保存")
    else:
        continue
    cv2.imshow('test',frame)
    cv2.waitKey(100)
# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()
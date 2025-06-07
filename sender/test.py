import cv2
import time




test=cv2.imread('./test.jpg')
cv2.namedWindow('test', cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow('test', 0,0)
cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow('test',test)
cv2.waitKey(60000)
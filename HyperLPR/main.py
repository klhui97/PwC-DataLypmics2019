from hyperlpr import *
import cv2

image = cv2.imread("t.jpg")
print(HyperLPR_PlateRecogntion(image))

i = 0
while i < 1000:
    image = cv2.imread("frames/frame" + str(i) + ".jpg")
    print(HyperLPR_PlateRecogntion(image))
    i += 1
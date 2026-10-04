import cv2 as cv 
import numpy as np
import matplotlib.pyplot as plt

image = cv.imread('Task 2/Input/6.jpeg')


#grayscale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

#blur
blur = cv.GaussianBlur(gray, (3,3), cv.BORDER_DEFAULT)

#canny
canny = cv.Canny(blur,50,150)
#graph
#plt.imshow(canny)
#plt.show()

#ROI
def ROI(image):
    traingle = np.array([[(320,548),(410,315),(855,548)]])
    mask = np.zeros_like(image)
    cv.fillPoly(mask, traingle, 255)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv.line(line_image, (x1,y1), (x2,y2), (128,0,255), 10)
    return line_image


roi = ROI(canny)
lane_image = np.copy(image)
lines = cv.HoughLinesP(roi,1, np.pi/180, 20, np.array([]), minLineLength=15, maxLineGap=20)
lane_image = display_lines(lane_image, lines)
final_image = cv.addWeighted(image, 0.8, lane_image, 1, 1)
#average_lines = average_slope(lane_image,lines)
cv.imshow('final', final_image)
#cv.imshow('result', lane_image)
#cv.imshow('canny', canny)
#cv.imshow  ('ROI', ROI(canny))
cv.imwrite('Task 2/Output/6.png', final_image)
cv.waitKey(0)
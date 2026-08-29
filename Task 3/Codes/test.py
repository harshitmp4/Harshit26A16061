import cv2 as cv
import numpy as np

image = cv.imread('Harshit26A16061/Task 3/Input/10.png')

#HSV
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
h, s, v = cv.split(hsv)
#cv.imshow('image', hsv)

potholes = []
obstacles = []

pothole_mask = cv.inRange(s, 0, 60) & cv.inRange(v, 140, 255)
#cv.imshow('pothole_mask', pothole_mask)

obstacle_mask = cv.inRange(s, 60, 255) & cv.inRange(v, 40, 255)
#cv.imshow('obstacle_mask', obstacle_mask)

#find pothole contours
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
mask = cv.morphologyEx(pothole_mask, cv.MORPH_OPEN, kernel)
mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
#cv.imshow('mask', mask)

contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#find obstacle contours 
kernel2 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
obstacle_mask_clean = cv.morphologyEx(obstacle_mask, cv.MORPH_OPEN, kernel2)
obstacle_mask_clean = cv.morphologyEx(obstacle_mask_clean, cv.MORPH_CLOSE, kernel2)

obstacle_contours, _ = cv.findContours(obstacle_mask_clean, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#filter obstacles
for cnt in obstacle_contours:
    area = cv.contourArea(cnt)
    x, y, w, h = cv.boundingRect(cnt)
    if area < 80:
        continue
    obstacles.append((x, y, w, h))

#filter potholes
for cnt in contours:
    area = cv.contourArea(cnt)
    x, y, w, h = cv.boundingRect(cnt)
    perimeter = cv.arcLength(cnt, True)
    circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
    if area < 300:
        continue
    if circularity < 0.4:
        continue
    potholes.append((x, y, w, h))

#mark potholes and obstacles on the image
for (x, y, w, h) in potholes:
    cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv.putText(image, f"({x},{y})", (x, y - 8), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

for (x, y, w, h) in obstacles:
    cv.rectangle(image, (x, y), (x + w, y + h), (255, 128, 0), 2)
    cv.putText(image, f"({x},{y})", (x, y - 8), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

print(f"Potholes: {len(potholes)}, Obstacles: {len(obstacles)}, Total: {len(potholes)+len(obstacles)}")

cv.imshow('result', image)
cv.imwrite('Harshit26A16061/Task 3/Output/result10.png', image)
cv.waitKey(0)


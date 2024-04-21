import cv2 as cv

img = cv.imread('./ejemplos/antigua.jpg')
cv.imshow('Park', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

blur = cv.GaussianBlur(img, (7,7), cv.BORDER_DEFAULT)
cv.imshow('Blur', blur)

canny = cv.Canny(blur, 125, 175)
cv.imshow('Canny Edges', canny)

dilated = cv.dilate(canny, (7,7), iterations=3)
cv.imshow('Dilated', dilated)

eroded = cv.erode(dilated, (7,7), iterations=3)
cv.imshow('Eroded', eroded)

resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow('Resized', resized)

cropped = img[50:200, 200:400]
cv.imshow('Cropped', cropped)

# https://github.com/jasmcaus/opencv-course/blob/master/Section%20%231%20-%20Basics/basic_functions.py
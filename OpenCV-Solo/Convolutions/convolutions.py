import cv2

image = cv2.imread("./ejemplos/Antigua.jpg")
# CONSTANTES PREDEFINIDAS ----------------------------- MAYUSCULAS
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur_image = cv2.GaussianBlur(image, (5, 5), 0)
edges = cv2.Canny(image, 100, 200)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow("Grayscale Image", gray_image)
cv2.imshow("Blurred Image", blur_image)
cv2.imshow("Edges", edges)
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
cv2.imshow("Contours", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# https://github.com/jasmcaus/opencv-course/blob/master/Section%20%231%20-%20Basics/basic_functions.py
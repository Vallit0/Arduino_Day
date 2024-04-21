import cv2
import numpy as np

############# 'Leer' imagenes
#
################# 'Leer' Videos
# video = cv2.VideoCapture('./ejemplos/cachorritos.mp4')

# while True:
#     ret, frame = video.read()
#     if not ret:
#         break

#     cv2.imshow('Video', frame)
#     if cv2.waitKey(1) == ord('q'):
#         break

# video.release()
# cv2.destroyAllWindows()

################ Leer Webcam
# video = cv2.VideoCapture(0)

# while True:
#     ret, frame = video.read() # frame es un objeto 
#     if not ret:
#         break

#     cv2.imshow('Webcam', frame)
#     if cv2.waitKey(1) == ord('q'):
#         break

# video.release()
# cv2.destroyAllWindows()

############# Dibujar "Cajitas"
# Dibujar "Cajitas"
# Create a black image with a size of 400x400 pixels
# image = np.zeros((400, 400, 3), dtype=np.uint8)

# cv2.rectangle(image, (50, 50), (200, 200), (0, 255, 0), 2)
# cv2.circle(image, (300, 150), 50, (0, 0, 255), -1)
# cv2.line(image, (100, 300), (300, 300), (255, 0, 0), 3)
# cv2.putText(image, 'Hello, OpenCV!', (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
# cv2.imshow('Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
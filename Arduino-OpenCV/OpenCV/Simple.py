import cv2
import mediapipe as mp
import time
import math
import serial

# Función para calcular distancia entre dos puntos
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Configuración inicial de MediaPipe y cámara
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
ser = serial.Serial('COM5', 9600) 

finger_tips = {
    'Pulgar': 4,
    'Índice': 8,
    'Medio': 12,
    'Anular': 16,
    'Meñique': 20
}

pTime = 0
touch_threshold = 50  # Umbral para considerar que los dedos se están tocando

# Bucle principal para procesa-miento de video
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            tip_positions = {}
            for finger, tip_id in finger_tips.items():
                lm = handLms.landmark[tip_id]
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                tip_positions[finger] = (cx, cy)
                cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

            
            if calculate_distance(*tip_positions['Índice'], *tip_positions['Pulgar']) < touch_threshold:
                ser.write(b'A')
            elif calculate_distance(*tip_positions['Medio'], *tip_positions['Pulgar']) < touch_threshold:
                ser.write(b'B')
            elif calculate_distance(*tip_positions['Anular'], *tip_positions['Pulgar']) < touch_threshold:
                ser.write(b'C')
            elif calculate_distance(*tip_positions['Meñique'], *tip_positions['Pulgar']) < touch_threshold:
                ser.write(b'D')

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

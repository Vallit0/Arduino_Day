import cv2
import mediapipe as mp
import time
import math
import requests  # Importar para hacer las peticiones HTTP

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

finger_tips = {
    'Pulgar': 4,
    'Índice': 8,
    'Medio': 12,
    'Anular': 16,
    'Meñique': 20
}

pTime = 0
touch_threshold = 50  # Umbral para considerar que los dedos se están tocando
text_positions = {}   # Diccionario para almacenar posiciones de texto para evitar superposiciones

# Estado inicial del ventilador
fan_state = False

# Función para encender o apagar el ventilador a través del ESP32
def control_fan(state):
    if state == "on":
        requests.get("http://192.168.4.1/fan/on")
    elif state == "off":
        requests.get("http://192.168.4.1/fan/off")

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            tip_positions = {}
            text_positions.clear()  # Limpiar posiciones de texto anteriores
            for finger, tip_id in finger_tips.items():
                lm = handLms.landmark[tip_id]
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                tip_positions[finger] = (cx, cy)
                cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

            # Verificar cada par de dedos para ver si se están tocando
            touching_messages = []
            for finger1, pos1 in tip_positions.items():
                for finger2, pos2 in tip_positions.items():
                    if finger1 != finger2 and (finger2, finger1) not in touching_messages:
                        distance = calculate_distance(pos1[0], pos1[1], pos2[0], pos2[1])
                        if distance < touch_threshold:
                            cv2.line(img, pos1, pos2, (0, 255, 0), 3)
                            message = f'{finger1} tocando {finger2}'
                            touching_messages.append((finger1, finger2))
                            if message not in text_positions:
                                text_positions[message] = (10, 70 + 30 * len(text_positions))
                            cv2.putText(img, message, text_positions[message], cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                            # Encender el ventilador cuando los dedos Pulgar e Índice se toquen
                            if (finger1 == 'Pulgar' and finger2 == 'Índice') or (finger1 == 'Índice' and finger2 == 'Pulgar'):
                                if not fan_state:
                                    control_fan("on")  # Encender ventilador
                                    fan_state = True
                            else:
                                if fan_state:
                                    control_fan("off")  # Apagar ventilador
                                    fan_state = False

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

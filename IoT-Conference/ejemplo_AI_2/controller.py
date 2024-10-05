import cv2
import mediapipe as mp
import time
import math
import serial  # Import PySerial

# Configure serial communication (replace 'COM3' with the correct port)
ser = serial.Serial('COM4', 115200, timeout=1)

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

finger_tips = {
    'Pulgar': 4,
    'Índice': 8
}

touch_threshold = 50  # Threshold for finger touch detection
motor_direction = "center"  # Initial state of the motor

# Function to control the motor using serial
def control_motor(direction):
    if direction == "left":
        ser.write(b'left\n')  # Send 'left' command over serial
    elif direction == "right":
        ser.write(b'right\n')  # Send 'right' command over serial

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

            # Check if the Thumb and Index are touching
            distance = calculate_distance(tip_positions['Pulgar'][0], tip_positions['Pulgar'][1],
                                          tip_positions['Índice'][0], tip_positions['Índice'][1])
            if distance < touch_threshold:
                if motor_direction != "left":  # Only send command if state changes
                    control_motor("left")
                    motor_direction = "left"
            else:
                if motor_direction != "right":  # Only send command if state changes
                    control_motor("right")
                    motor_direction = "right"

    # Show image in window
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()  # Close the serial connection when done

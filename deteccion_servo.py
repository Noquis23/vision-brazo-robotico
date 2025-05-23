import cv2
import mediapipe as mp
import serial  # Para enviar datos al Arduino
import time

# Abrimos conexión serial (ajusta el puerto COM según tu sistema)
arduino = serial.Serial('COM6', 9600)  # Cambia COM3 por el que tenga tu Arduino
time.sleep(2)  # Espera a que se establezca la conexión

# Inicializamos MediaPipe y la cámara
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
dedos_puntas = [8, 12, 16, 20]

cap = cv2.VideoCapture(0)

ultimo_dedo = -1  # Para no enviar siempre lo mismo

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb)

    dedos_arriba = 0

    if resultado.multi_hand_landmarks:
        for mano in resultado.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, mano, mp_hands.HAND_CONNECTIONS)
            landmarks = mano.landmark

            if landmarks[4].x < landmarks[3].x:
                dedos_arriba += 1

            for punta in dedos_puntas:
                if landmarks[punta].y < landmarks[punta - 2].y:
                    dedos_arriba += 1

            # Enviar al Arduino si cambia
            if dedos_arriba != ultimo_dedo:
                arduino.write(str(dedos_arriba).encode())  # Enviamos un número como string
                print(f"Enviado al Arduino: {dedos_arriba}")
                ultimo_dedo = dedos_arriba

            cv2.putText(frame, f'Dedos arriba: {dedos_arriba}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow('Contador de dedos + Servo', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()

# Par con servo2.txt
import cv2
import mediapipe as mp
import serial
import time

arduino = serial.Serial('COM3', 9600)  # Cambia COM3 si es necesario
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
dedos_puntas = [8, 12, 16, 20]

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
            lm = mano.landmark

            if lm[4].x < lm[3].x:
                dedos_arriba += 1

            for punta in dedos_puntas:
                if lm[punta].y < lm[punta - 2].y:
                    dedos_arriba += 1

            # Lógica de comandos por gesto
            if dedos_arriba == 0:
                comando = "GARRA_CERRAR"
            elif dedos_arriba == 5:
                comando = "GARRA_ABRIR"
            elif dedos_arriba == 1:
                comando = "GIRO_IZQUIERDA"
            elif dedos_arriba == 2:
                comando = "GIRO_DERECHA"
            elif dedos_arriba == 3:
                comando = "SUBIR_BRAZO"
            elif dedos_arriba == 4:
                comando = "BAJAR_BRAZO"
            else:
                comando = "NINGUNO"

            arduino.write((comando + "\n").encode())
            time.sleep(0.1)

            cv2.putText(frame, comando, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow('Gestos', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()

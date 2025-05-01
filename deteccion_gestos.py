import cv2
import mediapipe as mp

# Inicializamos MediaPipe y la cámara
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

# Índices de los puntos de referencia de las puntas de los dedos
dedos_puntas = [8, 12, 16, 20]  # índice, medio, anular, meñique

cap = cv2.VideoCapture(0)

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

            # Pulgar (comparamos eje X porque gira hacia un lado)
            if landmarks[4].x < landmarks[3].x:
                dedos_arriba += 1

            # Otros dedos (comparar punta con articulación inferior)
            for punta in dedos_puntas:
                if landmarks[punta].y < landmarks[punta - 2].y:
                    dedos_arriba += 1

            # Mostramos la cantidad
            cv2.putText(frame, f'Dedos arriba: {dedos_arriba}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow('Contador de dedos', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

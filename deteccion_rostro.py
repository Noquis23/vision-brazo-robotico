import cv2
import mediapipe as mp

# Inicializamos MediaPipe para la detección de rostros
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Configuramos el detector de rostros
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertimos la imagen a RGB (MediaPipe usa este formato)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesamos la imagen para detectar rostros
    result = face_detection.process(rgb_frame)

    # Si se detectan rostros, los dibujamos
    if result.detections:
        for detection in result.detections:
            # Dibujamos el rostro detectado
            mp_drawing.draw_detection(frame, detection)

    # Mostramos la imagen con los rostros detectados
    cv2.imshow('Detección de Rostros', frame)

    # Romper el ciclo si presionamos 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Par con servo3.txt
import cv2
import serial
import numpy as np

# Puerto y velocidad
COM = 'COM3'
BAUD = 9600
ser = serial.Serial(COM, BAUD)

cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while True:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilatada = cv2.dilate(thresh, None, iterations=3)

    contornos, _ = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contornos:
        area = cv2.contourArea(c)
        if area < 2000:
            continue

        x, y, w, h = cv2.boundingRect(c)
        centro_x = x + w // 2
        centro_y = y + h // 2
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # --- BASE: Movimiento horizontal ---
        if centro_x < 200:
            ser.write(b'izq1\n')
        elif centro_x < 420:
            ser.write(b'izq2\n')
        elif centro_x < 520:
            ser.write(b'izq3\n')
        elif centro_x < 650:
            ser.write(b'ctr\n')
        elif centro_x < 860:
            ser.write(b'der3\n')
        elif centro_x < 1080:
            ser.write(b'der2\n')
        else:
            ser.write(b'der1\n')

        # --- BRAZO: Movimiento vertical ---
        if centro_y < 150:
            ser.write(b'arriba\n')
        elif centro_y > 350:
            ser.write(b'abajo\n')

        # --- GARRA: Según tamaño del área ---
        if area > 10000:
            ser.write(b'cerrar\n')
        elif area < 5000:
            ser.write(b'abrir\n')

        break  # Solo controlamos con el primer movimiento fuerte encontrado

    cv2.imshow("Movimiento", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if not ret:
        break

    if cv2.waitKey(10) & 0xFF == ord('s'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()

import cv2

# Cargar el clasificador Haar para rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Cargar la imagen
img = cv2.imread('C:/Users/eusta/Downloads/rostros.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises

# Detectar rostros
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Dibujar rectángulos alrededor de los rostros detectados
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Mostrar la imagen con los rostros detectados
cv2.imshow('Rostros detectados', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

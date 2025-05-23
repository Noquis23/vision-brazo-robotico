#include <Servo.h>

Servo miServo;
int posicion;

void setup() {
  Serial.begin(9600);
  miServo.attach(9);  // Pin del servo
}

void loop() {
  if (Serial.available() > 0) {
    char dato = Serial.read();

    // Convertimos de carácter a número
    int dedos = dato - '0';

    // Mover el servo a diferentes posiciones según dedos
    switch (dedos) {
      case 0: posicion = 0; break;
      case 1: posicion = 30; break;
      case 2: posicion = 60; break;
      case 3: posicion = 90; break;
      case 4: posicion = 120; break;
      case 5: posicion = 150; break;
      default: posicion = 0;
    }

    miServo.write(posicion);
    delay(300);
  }
}

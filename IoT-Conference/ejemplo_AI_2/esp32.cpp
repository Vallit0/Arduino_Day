#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "ESP32-AP";
const char* password = "12345678";

WebServer server(80);

void setup() {
  Serial.begin(115200);  // Comunicación serial con el Arduino
  WiFi.softAP(ssid, password);
  Serial.print("Access Point iniciado. Dirección IP: ");
  Serial.println(WiFi.softAPIP());

  // Control para mover el motor a la izquierda
  server.on("/motor/left", []() {
    Serial.println("left");  // Enviar comando 'left' al Arduino
    server.send(200, "text/html", "Motor movido a la izquierda");
  });

  // Control para mover el motor a la derecha
  server.on("/motor/right", []() {
    Serial.println("right");  // Enviar comando 'right' al Arduino
    server.send(200, "text/html", "Motor movido a la derecha");
  });

  server.begin();
}

void loop() {
  server.handleClient();  // Manejar solicitudes entrantes
}

#include <WiFi.h>
#include <WebServer.h>
#include <Arduino.h>

const char* ssid = "ESP32-AP";
const char* password = "12345678";

WebServer server(80);

int IN1 = 17;
int IN2 = 16;

void controlFan(int state1, int state2);

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  controlFan(LOW, LOW);

  WiFi.softAP(ssid, password);
  Serial.print("Access Point iniciado. Dirección IP: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", []() {
    server.send(200, "text/html", "<h1>Bienvenido al servidor ESP32</h1>");
  });

  server.on("/fan/on", []() {
    controlFan(HIGH, LOW);
    server.send(200, "text/html", "Fan encendido");
  });

  server.on("/fan/off", []() {
    controlFan(LOW, LOW);
    server.send(200, "text/html", "Fan apagado");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}

void controlFan(int state1, int state2) {
  digitalWrite(IN1, state1);
  digitalWrite(IN2, state2);
}

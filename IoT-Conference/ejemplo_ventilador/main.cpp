#include <WiFi.h>
#include <WebServer.h>
#include <Arduino.h>

const char* ssid = "Conf. ECYS Orga"; // Nombre de la red WiFi
const char* password = "12345678"; // Contraseña de la red WiFi

WebServer server(80);

int IN1 = 17;
int IN2 = 16;

// Declaración de funciones
void controlFan(int state1, int state2);

// HTML para la página web
String webpage = "<html>\
  <head>\
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\
    <style>\
      body { font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; margin: 0; padding: 0; }\
      .container { max-width: 600px; margin: 50px auto; padding: 20px; background-color: #fff; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 10px; text-align: center; }\
      h1 { color: #4CAF50; margin-bottom: 20px; }\
      h2 { color: #333; font-size: 18px; margin-bottom: 40px; }\
      button { padding: 15px 25px; font-size: 18px; margin: 20px; cursor: pointer; border: none; border-radius: 5px; transition: background-color 0.3s; }\
      .on { background-color: #4CAF50; color: white; }\
      .on:hover { background-color: #45a049; }\
      .off { background-color: #f44336; color: white; }\
      .off:hover { background-color: #e41f1f; }\
      .footer { margin-top: 30px; font-size: 14px; color: #888; }\
    </style>\
  </head>\
  <body>\
    <div class='container'>\
      <h1>Bienvenido a la conferencia por Sebastian Valle</h1>\
      <h2>Escuela de Ciencias y Sistemas</h2>\
      <p>Control del ventilador:</p>\
      <button class='on' onclick='location.href=\"/on\"'>Encender</button>\
      <button class='off' onclick='location.href=\"/off\"'>Apagar</button>\
      <div class='footer'>Desarrollado con ESP32</div>\
    </div>\
  </body>\
</html>";

void setup() {
  // Configuración de los pines
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  controlFan(LOW, LOW); // Apagar ventilador inicialmente

  // Configuración del Access Point
  WiFi.softAP(ssid, password);
  Serial.println();
  Serial.print("Access Point iniciado. Dirección IP: ");
  Serial.println(WiFi.softAPIP());

  // Definir rutas para encender y apagar el ventilador
  server.on("/", []() {
    server.send(200, "text/html", webpage);
  });

  server.on("/on", []() {
    controlFan(HIGH, LOW); // Encender ventilador
    server.send(200, "text/html", webpage + "<p>Ventilador encendido.</p>");
  });

  server.on("/off", []() {
    controlFan(LOW, LOW); // Apagar ventilador
    server.send(200, "text/html", webpage + "<p>Ventilador apagado.</p>");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}

// Definición de funciones
void controlFan(int state1, int state2) {
  digitalWrite(IN1, state1);
  digitalWrite(IN2, state2);
}

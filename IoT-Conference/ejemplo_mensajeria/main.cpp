#include <WiFi.h>
#include <WebServer.h>
#include <Arduino.h>

// Configurar ESP32 en modo AP
const char* ssid = "ESP32-Foro";
const char* password = "12345678";

// Crear el servidor web en el puerto 80
WebServer server(80);

// Almacenamiento de mensajes (máximo 10 mensajes)
String messages[10];
int messageIndex = 0;

// Función para manejar el formulario de envío de mensajes
void handleMessageSubmit() {
  if (server.hasArg("message")) {
    String newMessage = server.arg("message");

    // Almacenar el mensaje en el arreglo (rotación si hay más de 10)
    messages[messageIndex] = newMessage;
    messageIndex = (messageIndex + 1) % 10;

    // Redirigir a la página principal después de enviar el mensaje
    server.sendHeader("Location", "/");
    server.send(303);
  }
}

// Página HTML para el foro
String generatePage() {
  String page = "<html>\
    <head>\
      <title>Foro ESP32</title>\
      <meta name='viewport' content='width=device-width, initial-scale=1.0'>\
      <style>\
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }\
        h1 { color: #4CAF50; }\
        .messages { background-color: white; padding: 10px; border-radius: 5px; margin-bottom: 20px; }\
        .message { padding: 5px; border-bottom: 1px solid #ddd; }\
        .message:last-child { border-bottom: none; }\
        form { margin-top: 20px; }\
        input[type='text'] { padding: 10px; width: 80%; font-size: 16px; }\
        input[type='submit'] { padding: 10px; font-size: 16px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }\
      </style>\
    </head>\
    <body>\
      <h1>Foro ESP32</h1>\
      <div class='messages'>";

  // Mostrar los mensajes almacenados
  for (int i = 0; i < 10; i++) {
    if (messages[i] != "") {
      page += "<div class='message'>" + messages[i] + "</div>";
    }
  }

  page += "</div>\
      <form action='/submit' method='POST'>\
        <input type='text' name='message' placeholder='Escribe tu mensaje aquí...' required>\
        <input type='submit' value='Enviar'>\
      </form>\
    </body>\
  </html>";

  return page;
}

// Manejador para la página principal
void handleRoot() {
  String page = generatePage();
  server.send(200, "text/html", page);
}

void setup() {
  Serial.begin(115200);

  // Configurar el ESP32 como AP
  WiFi.softAP(ssid, password);
  Serial.print("Access Point iniciado. Dirección IP: ");
  Serial.println(WiFi.softAPIP());

  // Definir manejadores para las rutas
  server.on("/", handleRoot);
  server.on("/submit", handleMessageSubmit);

  // Iniciar el servidor
  server.begin();
}

void loop() {
  server.handleClient();
}

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "INFINITUM0649";
const char* password = "467H3EGEvy";
const IPAddress espIP(192, 168, 1, 180);
const int espPort = 1234;

WiFiUDP Udp;

void setup() {
  Serial.begin(115200);
  Serial.println();
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  IPAddress gateway = WiFi.gatewayIP();
  IPAddress subnet = WiFi.subnetMask();

  WiFi.config(espIP, gateway, subnet);

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("IP: " + WiFi.localIP().toString());

  Udp.begin(espPort);
}

void loop() {
  uint8_t buffer[1024];
  int packetSize = Udp.parsePacket();

  if (packetSize) {
    Udp.read(buffer, sizeof(buffer));

    for (int i = 0; i < 1024; i++) {
      // Salida de audio a través del módulo LM386 (conexión al pin A0)
      analogWrite(A0, buffer[i]);
      delayMicroseconds(50);  // Ajusta según sea necesario
    }
  }
}

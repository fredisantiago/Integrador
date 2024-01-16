  #include <ESP8266WiFi.h>
  #include <WiFiUdp.h>
  const char* ssid = "INFINITUM0649";
  const char* password = "467H3EGEvy";
 
int contconexion = 0;

WiFiUDP Udp;

void setup()
{
  Serial.begin(115200);
  Serial.println();

  pinMode(5, OUTPUT);  //D1 Led de estado
  digitalWrite(15, LOW);

  WiFi.mode(WIFI_STA); //para que no inicie el SoftAP en el modo normal
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED and contconexion <50) { //Cuenta hasta 50 si no se puede conectar lo cancela
    ++contconexion;
    delay(250);
    Serial.print(".");
    digitalWrite(5, HIGH);
    delay(250);
    digitalWrite(5, LOW);
  }
  if (contconexion <50) {
      //para usar con ip fija
      IPAddress Ip(192,168,1,50); 
      IPAddress Gateway(192,168,1,254); 
      IPAddress Subnet(255,255,255,0); 
      WiFi.config(Ip, Gateway, Subnet); 
      
      Serial.println("");
      Serial.println("WiFi conectado");
      Serial.println(WiFi.localIP());
      digitalWrite(5, HIGH);  
  }
  else { 
      Serial.println("");
      Serial.println("Error de conexion");
      digitalWrite(15, LOW);
  }
}

void loop()
{
  Udp.beginPacket("192.168.1.68", 1234);

  for(int i=0; i<1024;i++){
    int old=micros();

    float analog = analogRead(17);

    analog = ((analog / 1) - 385);
    if (analog > 255){
      analog = 255;
    }
    else if (analog < 0){
      analog = 0;
    }
    
    Udp.write(int(analog));
    while(micros()-old<87); // 90uSec = 1Sec/11111Hz - 3uSec para los otros procesos
  }
  Udp.endPacket();
  delay(5);
}
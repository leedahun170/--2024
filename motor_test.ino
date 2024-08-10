#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi 설정
const char* ssid = "Dahun";
const char* password = "dlekgns1@"; // AjouUniv_PRIVATE 와이파이 비밀번호 입력

// MQTT 브로커 설정
const char* mqtt_server = "broker.hivemq.com"; // 공용 MQTT 브로커 사용 (로컬 브로커를 설정할 수도 있습니다)
const char* mqtt_topic = "ajou/led";

WiFiClient espClient;
PubSubClient client(espClient);

const int Pin_Dir = 3;
const int Pin_Speed = 4; // LED가 연결된 핀

void setup() {
  pinMode(Pin_Dir, OUTPUT);
  pinMode(Pin_Speed, OUTPUT);

  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(message);


}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("D1_R2_Client")) {
      Serial.println("connected");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  digitalWrite(Pin_Dir , HIGH);
  digitalWrite(Pin_Speed , HIGH);
  delay(10000);
  digitalWrite(Pin_Dir , LOW);
  digitalWrite(Pin_Speed , HIGH);
  Serial.print("test");
  



}

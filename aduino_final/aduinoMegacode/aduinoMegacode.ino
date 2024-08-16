String receivedMessage = "";
void setup() {
  Serial.begin(9600);       // 기본 시리얼 통신 (USB 연결용)
  Serial1.begin(9600);      // Serial1: RX1 -> 19, TX1 -> 18 (ESP8266과의 통신) / rx - D3, tx - D4
}

void loop() {
  // Serial1로부터 메시지를 수신
  if (Serial1.available()) {
    String receivedMessage = Serial1.readString(); // 수신된 메시지를 문자열로 저장
    Serial.println("Received from ESP8266: " + receivedMessage); // 메시지를 시리얼 모니터에 출력
  }
  //모터 구동 알고리즘
  //상하 모터제어
  if(receivedMessage[1] = d){
    
  }
 
}

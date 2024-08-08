import paho.mqtt.client as mqtt
import time

import paho.mqtt.publish as publish
topic = "dahun_test"
payload = "jebal"
broker = "mqtt.eclipseprojects.io"
port = 1883
client = mqtt.Client()
client.connect(broker,port)
client.loop_start()
try:
    while True:
        payload = "Hello, MQTT!"
        client.publish(topic, payload)
        print(f"Published '{payload}' to the topic '{topic}'")
        time.sleep(5)  # 5초마다 메시지 퍼블리시
except KeyboardInterrupt:
    print("Stopped by user")

# 네트워크 루프 종료 및 연결 종료
client.loop_stop()
client.disconnect()
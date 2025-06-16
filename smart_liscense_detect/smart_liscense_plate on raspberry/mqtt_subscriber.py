import paho.mqtt.client as mqtt
import json
from db_utils import insert_log
import base64
import cv2
import numpy as np
import os
import sqlite3


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected successfully!")
        client.subscribe("pi/license_plate")
    else:
        print(f"[MQTT] Connection failed with code {rc}")

def save_image(base64_str, timestamp):
    os.makedirs("logs/images", exist_ok=True)
    image_bytes = base64.b64decode(base64_str)
    np_img = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    filename = f"logs/images/plate_{timestamp.replace(':', '-')}.jpg"
    cv2.imwrite(filename, img)
    return filename

def on_message(client, userdata, msg):
    print(f"[MQTT] ?? Message received on topic: {msg.topic}")
    try:
        data = json.loads(msg.payload.decode())
        plate = data['plate']
        timestamp = data['timestamp']
        confidence = data['confidence']
        image_b64 = data.get('image')

        image_path = save_image(image_b64, timestamp) if image_b64 else None
        insert_log(plate, timestamp, confidence, image_path)
        print(f"[MQTT] ? Saved: {plate} at {timestamp} ? {image_path}")
    except Exception as e:
        print(f"[MQTT] ? Error: {e}")
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()

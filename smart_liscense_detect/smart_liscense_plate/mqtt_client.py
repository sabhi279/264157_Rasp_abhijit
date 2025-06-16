import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)

def publish_plate(plate, timestamp, confidence, image_base64):
    payload = json.dumps({
        "plate": plate,
        "timestamp": timestamp,
        "confidence": confidence,
        "image": image_base64
    })
    client.publish("pi/license_plate", payload)


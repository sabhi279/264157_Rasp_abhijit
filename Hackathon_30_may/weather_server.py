import socket
import json
from gpiozero import LED
 
led = LED(26)
HOST = '0.0.0.0'
PORT = 5001
THRESHOLD_TEMP = 30
 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Server listening on {HOST}:{PORT}")
 
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        if data:
            weather = json.loads(data.decode('utf-8'))
            temp = weather['temperature']
            pressure = weather['pressure']
            condition = weather['condition']
 
            print(f"Temp: {temp}°C")
            print(f"Press: {pressure} hPa")
            print(f"Cond: {condition}")
 
            if temp > THRESHOLD_TEMP:
                print("🔴 ALERT: High Temperature!")
                led.on()
            else:
                led.off()

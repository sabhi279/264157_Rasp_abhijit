import socket
import json
import requests
 
API_KEY = 'a3ceb4955c243795052cc5540846f547'
CITY = 'Kolkata'
RASPBERRY_PI_IP = '172.19.58.116'  # Replace with Pi IP
PORT = 5001
 
def get_weather():
    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
   
    if response.status_code != 200:
        print("❌ API Error:", data)
        return {}
   
    return {
        'temperature': data['main']['temp'],
        'pressure': data['main']['pressure'],
        'condition': data['weather'][0]['main']
    }
 
 
def send_data_to_pi(weather_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((RASPBERRY_PI_IP, PORT))
        s.sendall(json.dumps(weather_data).encode('utf-8'))
 
if __name__ == "__main__":
    weather = get_weather()
    send_data_to_pi(weather)
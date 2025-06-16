import cv2
import base64
from datetime import datetime
from ocr_utils import extract_plate_text
from mqtt_client import publish_plate
import easyocr
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

reader = easyocr.Reader(['en'], gpu=False)

def encode_image(image):
    """Encode image as base64 JPEG string."""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

def test_image_detection(image_path):
    print(f"📂 Loading image: {image_path}")
    frame = cv2.imread(image_path)

    if frame is None:
        print("❌ Could not load image.")
        return

    print(f"📏 Original image size: {frame.shape}")
    print("🧠 Running OCR on full image...")

    # Optional: preview/save raw image
    cv2.imwrite("full_input_preview.jpg", frame)

    # Raw OCR preview (optional debug)
    raw_results = reader.readtext(frame)
    print("\n🔍 Raw OCR Detected Texts:")
    for _, text, conf in raw_results:
        print(f"- '{text}' (Confidence: {conf:.2f})")

    # Filtered, formatted plate detection
    plates = extract_plate_text(frame)

    if not plates:
        print("⚠️ No valid plate detected.")
        return

    image_data = encode_image(frame)

    for text, conf in plates:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        print(f"✅ Detected Plate: {text} - {conf:.2f}")
        publish_plate(text, timestamp, conf, image_data)
        print(f"📤 Published plate: {text}")
try:
    client.publish(MQTT_TOPIC, payload)
    print(f"📤 Published: {text}")
except Exception as e:
    print(f"❌ MQTT Publish Error: {e}")



if __name__ == "__main__":
    test_image_detection("test_plate.jpg")  # Replace with your filename

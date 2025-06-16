import easyocr
import cv2

img = cv2.imread("test_plate.jpg")  # Make sure this file exists
reader = easyocr.Reader(['en'], gpu=False)
results = reader.readtext(img)

for bbox, text, confidence in results:
    print(f"Detected: {text} (Confidence: {confidence:.2f})")

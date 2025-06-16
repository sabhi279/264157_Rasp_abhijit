import easyocr
import cv2

# Load image from webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if not ret:
    print("Failed to capture image from webcam.")
    exit()

# Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)  # Force CPU since no CUDA

# Run OCR
results = reader.readtext(frame)

# Print results
for bbox, text, confidence in results:
    print(f"Detected: {text} (Confidence: {confidence:.2f})")

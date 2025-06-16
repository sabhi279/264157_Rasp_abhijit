import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=False)

img = cv2.imread('test_plate.jpg')
results = reader.readtext(img)

print("\nDetected text:")
for bbox, text, confidence in results:
    print(f"{text} ({confidence:.2f})")

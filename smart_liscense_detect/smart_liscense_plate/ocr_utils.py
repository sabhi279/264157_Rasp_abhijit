import easyocr
import re
import itertools

reader = easyocr.Reader(['en'], gpu=False)

# Indian license plate format: TN37CS2765, KA51MK4666, MH12AB1234
plate_pattern = re.compile(r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$')

def extract_plate_text(image):
    results = reader.readtext(image)

    print("🔍 Raw OCR Detected Texts:")
    for _, text, conf in results:
        print(f"- '{text}' (Confidence: {conf:.2f})")

    lines = []
    for (_, text, conf) in results:
        clean = text.replace(" ", "").upper()
        if conf > 0.4 and len(clean) >= 2:
            lines.append(clean)

    if not lines:
        return []

    print(f"🧠 Cleaned OCR Lines: {lines}")
    valid_plates = []

    # Try all 2 to 4-line combinations
    for n in range(2, min(5, len(lines)+1)):
        for combo in itertools.permutations(lines, n):
            combined = ''.join(combo)
            if plate_pattern.match(combined):
                print(f"✅ Matched Combo: {combined}")
                valid_plates.append((combined, 1.0))
                return valid_plates  # stop at first valid match

    print("⚠️ No valid plate detected.")
    return []

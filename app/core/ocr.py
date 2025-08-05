from PIL import Image
import pytesseract
import io
import base64

def extract_text_from_base64(image_base64):
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    try:
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

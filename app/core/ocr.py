from PIL import Image
import pytesseract
import io
import base64

def extract_text_from_base64(image_base64):
    image_data = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return text.strip()

import pdfplumber
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            text = ''.join([page.extract_text() or '' for page in pdf.pages])
        if not text.strip():
            return extract_text_with_ocr(file)
        return text
    except Exception as e:
        print("Error:", e)
        return extract_text_with_ocr(file)

def extract_text_with_ocr(file):
    images = convert_pdf_to_images(file)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def convert_pdf_to_images(file):
    from pdf2image import convert_from_bytes
    return convert_from_bytes(file.read())

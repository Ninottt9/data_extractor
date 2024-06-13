import cv2
import pytesseract
import matplotlib.pyplot as plt
import re

# Load and preprocess the image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.medianBlur(thresh, 3)
    return denoised

# OCR processing function
def ocr_process(image):
    # custom_config = r'--oem 3 --psm 6'
    # custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789./'
    custom_config = ''
    text = pytesseract.image_to_string(image, config=custom_config, lang='eng+pol')
    return text

# Function to clean and standardize OCR output
def clean_ocr_text(text):
    text = re.sub(r'[~:"]', '', text)
    text = re.sub(r'\s+', ' ', text)  # Remove excessive whitespace
    text = re.sub(r'[^a-zA-Z0-9\s./]', '', text)  # Remove unwanted characters
    return text

# Function to extract key fields from the text
def extract_fields(text):
    fields = {}
    
    patterns = {
        'SURNAME': r'Nazwisko / SURNAME\s*(\w+)',
        'GIVEN NAMES': r'IMIONA / GIVEN NAMES\s*(\w+)',
        'NATIONALITY': r'OBYWATELSTWO / NATIONALITY\s*(\w+)',
        'DATE OF BIRTH': r'DATA URODZENIA / DATE OF BIRTH\s*(\d{1,2}\.\d{1,2}\.\d{4})',
        'IDENTITY CARD NUMBER': r'NUMER DOWODU OSOBISTEGO/ IDENTITY CARD NUMBER\s*(\w+)',
        'SEX': r'PŁEĆ / SEX\s*([MF])',
        'EXPIRY DATE': r'TERMIN WAŻNOŚCI / EXPIRY DATE\s*(\d{1,2}\.\d{1,2}\.\d{4})'
    }
    
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[field] = match.group(1)
    
    return fields

# Generic function to process multiple documents
def process_documents(image_paths):
    results = []
    for path in image_paths:
        preprocessed_image = preprocess_image(path)
        ocr_output = ocr_process(preprocessed_image)
        cleaned_text = clean_ocr_text(ocr_output)
        fields = extract_fields(cleaned_text)
        results.append(fields)
    return results

if __name__ == '__main__':
    # Load and preprocess the image
    image_path = r'D:/Uczenie\AGH/2_STOPIEN/SEM_1/AIPO/projekt/documents_processor/generated/document_15.png'
    processed_image = preprocess_image(image_path)

    # Perform OCR on the preprocessed image
    ocr_text = ocr_process(processed_image)
    print('ocr_text')
    print(ocr_text)

    # Clean and standardize the OCR output
    cleaned_text = clean_ocr_text(ocr_text)
    print('cleaned_text')
    print(cleaned_text)

    # Extract key fields from the cleaned text
    fields = extract_fields(cleaned_text)
    print('extracted fields')
    # Display the extracted fields
    for key, value in fields.items():
        print(f"{key}: {value}")

    # Example of processing multiple documents
    # image_paths = ['path_to_your_image1.png', 'path_to_your_image2.png']
    # document_fields = process_documents(image_paths)
    # for fields in document_fields:
    #   for key, value in fields.items():
    #     print(f"{key}: {value}")
    #   print("---")
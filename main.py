import cv2
import pytesseract
import matplotlib.pyplot as plt
import re
import os
import argparse

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
    custom_config = ''
    text = pytesseract.image_to_string(image, config=custom_config, lang='eng+pol')
    return text

# Function to clean and standardize OCR output
def clean_ocr_text(text):
    text = re.sub(r'[~:"]', '', text)
    text = re.sub(r'\s+', ' ', text)  # Remove excessive whitespace
    text = re.sub(r'[^a-zA-Z0-9\s./]', '', text)  # Remove unwanted characters
    text = re.sub(r':', '', text) # remove colons
    text = re.sub(r'([a-zA-Z])\.', r'\1', text) # remove dots after letters
    return text

# Function to extract key fields from the text
def extract_fields(text):
    fields = {}
    
    patterns = {
        'SURNAME': r'SURNAME\s*([A-Z]+)',
        'GIVEN NAMES': r'GIVEN NAMES\s*([A-Z]+)',
        'NATIONALITY': r'.*(POLSKIE)',
        'DATE OF BIRTH': r'DATE OF BIRTH\s*|POLSKIE\s*(\d{1,2}\.\d{1,2}\.\d{4})',
        'IDENTITY CARD NUMBER': r'CARD NUMBER\s*([A-Z]{3}\s\d{6})',
        'SEX': r'.*(\s+[KM]\s+)',
        'EXPIRY DATE': r'EXPIRY DATE\s*(\d{1,2}\.\d{1,2}\.\d{4})'
    }
    
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[field] = match.group(1)
    
    return fields

# Function to process all images in a given folder and save results
def process_documents_in_folder(folder_path, output_folder):
    results = []
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # List all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().startswith('document') and filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_path = os.path.join(folder_path, filename)
            preprocessed_image = preprocess_image(image_path)
            ocr_output = ocr_process(preprocessed_image)
            cleaned_text = clean_ocr_text(ocr_output)
            # spell_checked_text = spell_check(cleaned_text)
            fields = extract_fields(cleaned_text)
            document_name = os.path.splitext(filename)[0]
            save_results_to_file(fields, output_folder, document_name)
            results.append(fields)
    return results

# Function to save extracted fields to a text file
def save_results_to_file(fields, output_folder, document_name):
    output_path = os.path.join(output_folder, f"{document_name}.txt")
    with open(output_path, 'w') as f:
        for key, value in fields.items():
            f.write(f"{key}: {value}\n")
            
def main():
    parser = argparse.ArgumentParser(description="Process OCR on document images.")
    parser.add_argument('-i', '--input_folder', required=True, help="Path to the input folder containing images.")
    parser.add_argument('-o', '--output_folder', required=True, help="Path to the output folder to save results.")
    args = parser.parse_args()

    process_documents_in_folder(args.input_folder, args.output_folder)


if __name__ == '__main__':
    main()
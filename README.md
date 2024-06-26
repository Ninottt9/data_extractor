# Document Processor Module
Extracts face image and the corresponding data from the documents.

## Usage
- ```python main.py -i <input_folder> -o <input_folder>```
alternatively
- ```python main.py --input_folder <input_folder> --output_folder <output_folder>```
Where input_folder is the folder containing the documents and output_folder is the folder where the extracted data will be stored (in the format: document_name_extracted_img.jpg, document_name.txt).
The image is the extracted face, and the text file contains the extracted data in ```key=value``` format.

For 30 images, it takes approximately 1 minute to for the program to run.

## Output
The output is stored in the output folder in the format: document_name_extracted_img.jpg, document_name.txt.
The image is the extracted face, and the text file contains the extracted data in ```key=value``` format.
The data key values are:
For the ID card:
- SURNAME
- GIVEN_NAMES
- NATIONALITY
- DATE_OF_BIRTH
- IDENTITY_CARD_NUMBER
- SEX
- EXPIRY_DATE
- DOCUMENT_TYPE=NATIONAL_ID (this field is always present)

For the Passport:
- SURNAME
- GIVEN_NAMES
- COUNTRY
- DATE_OF_BIRTH
- SEX
- DATE_OF_ISSUE
- EXPIRY_DATE
- DOCUMENT_TYPE=PASSPORT (this field is always present)

The data may be incomplete or incorrect.
If the document type is not recognized, no data will be extracted and the image will appear on the console: ```Document type not recognized for <document_name>```.

## Requirements
- python 3.6+
- tessaract

## installation
- install pytesseract: https://pypi.org/project/pytesseract/
- install polish and englisgh language packs for tessaract: https://ocrmypdf.readthedocs.io/en/latest/languages.html
- ```pip install -r requirements.txt```

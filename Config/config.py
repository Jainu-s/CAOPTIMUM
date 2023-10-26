import spacy
from PIL import Image
import pytesseract

'''
This code defines functions for natural language processing (NLP) using the spaCy library and
for extracting text from an image using the Tesseract OCR (Optical Character Recognition) engine. 
The load_model function initializes an NLP model, and the extract_text_from_image function extracts
text from an image file. The code also configures Tesseract for image text extraction.
'''
# NLP Code
nlp = None

def load_model():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")
    return nlp



from PIL import Image
import pytesseract

# Only required if Tesseract is not added to your PATH (especially for Windows users)
# Update the path to the Tesseract executable if it's different on your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def extract_text_from_image(image_path):
    """Extracts text from the specified image.

    Args:
    - image_path (str): Path to the image file.

    Returns:
    - str: Extracted text from the image.
    """


    # Open the image file
    image = Image.open(image_path)

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(image)

    return text


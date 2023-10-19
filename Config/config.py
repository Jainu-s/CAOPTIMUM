import spacy
from PIL import Image
import pytesseract


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


# # Example usage:
# image_path = r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Scripts\Screenshot\SW101\9SW101click.png'  # Replace with your image path
# extracted_text = extract_text_from_image(image_path)
# print(extracted_text)

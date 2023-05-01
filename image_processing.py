import os
from typing import Tuple, Union
from PIL import Image
from pytesseract import pytesseract

#Set path to where your tesseract.exe is located
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

"""
Function that performs OCR on image, grabbing all text from it as possible
:param image: the image to perform OCR on, and extract text out of
:return: a string that holds all the text grabbed from the image
"""
def ocr_image(image) -> str:
    text = pytesseract.image_to_string(image)
    text = text.lower()
    return text


"""
Function that processes if a message contains an image attachment
:param message: represents the message that is to be processed, to see if it contains an image attachment
:return: A boolean that is True if image has been processed, for False otherwise, and an image/None
"""
async def capture_image(message) -> Tuple[bool, Union[Image.Image, None]]:
    # Check if message has attachment
    if message.attachments:
        for attachment in message.attachments:
            # Check if attachment is img (jpg / png)
            if attachment.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Save image locally
                save_directory = 'Images'
                # exist_ok=True means that function won't raise error if directory already exists
                os.makedirs(save_directory, exist_ok=True)
                image_path = os.path.join(save_directory, attachment.filename)
                await attachment.save(image_path)
                await message.channel.send(f"Image saved as {attachment.filename}")
                # Open image using PIL (so can return an img)
                img = Image.open(image_path)
                return True, img
    return False, None

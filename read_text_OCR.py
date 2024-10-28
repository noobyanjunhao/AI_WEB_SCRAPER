#python3 -m pip install beautifulsoup4 requests opencv-python pillow tesseract pytesseract

from PIL import Image
import pytesseract
import os

# Function to extract all text from an image
def extract_text_from_image(image_path):
    # Load the image
    image = Image.open(image_path)
    
    # Apply OCR to extract text
    text = pytesseract.image_to_string(image)
    
    return text

# Function to save extracted text to a .txt file
def save_extracted_text(text, output_path):
    # Write the extracted text to a .txt file
    with open(output_path, 'w') as file:
        file.write(text)
    
    print(f"Extracted text saved at {output_path}")


# Folder containing existing screenshots to process
image_folder = 'screenshots/screenshots_20241025_011521'
image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith('.png')]

output_folder = 'extracted_text/screenshots_20241025_011521'
#create one if not exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process each image and save the extracted text 
for path in image_paths:
    text = extract_text_from_image(path)
    
    # Define the output file path based on the image name
    filename = os.path.basename(path).replace(".png", ".txt")
    output_path = os.path.join(output_folder, filename)
    
    # Save the extracted text to a file
    save_extracted_text(text, output_path)


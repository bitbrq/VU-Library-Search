import fitz  # PyMuPDF
import os
import re
from langdetect import detect

def visitor_body(text, parts):
    try:
        parts.append(text)
    except IndexError:
        print("Invalid input")

def filter_english_words(text):
    english_words = []
    words = text.split()
    for word in words:
        try:
            if detect(word) == 'en':  # Check if word is English
                english_words.append(word)
        except:
            pass  # Skip words that cause language detection errors
    return ' '.join(english_words)

if __name__ == '__main__':
    # Loop through PDF files in the directory
    for filename in os.listdir("Books"):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join("Books", filename)
            output_filename = os.path.splitext(filename)[0] + ".txt"  # Use PDF filename for the output text filename
            if os.path.exists(os.path.join("TextBooks", output_filename)):
                print("All Files in Books are Already converted to text.")
            else:
                # Open a text file for writing
                output_directory = "TextBooks"
                os.makedirs(output_directory, exist_ok=True)
                with open(os.path.join("TextBooks", output_filename), "w", encoding="utf-8") as f:
                    # Open the PDF file
                    pdf_document = fitz.open(pdf_path)
                    num_pages = pdf_document.page_count
                    parts = []
                    print("Conversion process Started Please wait...")
                    # Iterate through all pages
                    for page_number in range(num_pages):
                        page = pdf_document[page_number]

                        # Extract text from each page
                        text = page.get_text("text")
                        text = re.sub(r'\n+', '\n', text)  # Remove excess enter spacescleaned_text = re.sub(r'[^A-Za-z\s]', '', text)
                        text = text.lower()
                        text = re.sub(r'\s+', ' ', text).strip()
                        visitor_body(text, parts)

                    # Concatenate the extracted text parts
                    text_body = "\n".join(parts)

                    # Write the text to the text file
                    f.write(text_body)
print("Conversion Completed Successfully.")

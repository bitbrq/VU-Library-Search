import fitz  # PyMuPDF
import os
import re


def visitor_body(text, parts, cm, tm, font_dict, font_size):
    try:
        parts.append(text)
    except IndexError:
        print("Invalid input")


if __name__ == '__main__':
    # Loop through PDF files in the directory
    for filename in os.listdir("books"):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join("books", filename)
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
                        text = re.sub(r'[^A-Za-z\s]', '', text)
                        text = text.lower()
                        visitor_body(text, parts, [], [], {}, 0)

                    # Concatenate the extracted text parts
                    text_body = "".join(parts)

                    # Write the text to the text file
                    f.write(text_body)
print("Conversion Completed Successfully.")

# Make sure to install PyMuPDF:
# pip install PyMuPDF

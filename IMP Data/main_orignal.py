import os
import PyPDF2
import string
from multiprocessing import Pool, cpu_count


def get_pdf_dir():
    # Function to get the directory containing PDF files
    print("Default Path for PDF files is '/Books'.")
    user_selection = input("Would you like to change path for PDF Files? Press 'y' for yes, or 'n' for no. : ")
    if user_selection == 'y':
        pdf_dir = input("Press Enter your Directory Address Where PDF Files are Located...")
    else:
        pdf_dir = "../Books"
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
            print(f"Created directory {pdf_dir}")
            print("Books Directory Created Please Place file in it")
        print("PDF Directory Found.")
        input("Press Enter to Continue...")
    return pdf_dir


def get_index_dir():
    # Function to get the directory containing the Index file
    print("Default Path for Index file is '/Index'.")
    user_selection = input("Would you like to change path for Index File? Press 'y' for yes, or 'n' for no. : ")
    if user_selection == 'y':
        index_dir = input("Press Enter your Directory Address Where Index File is Located...")
    else:
        index_dir = "../Index"
        if not os.path.exists(index_dir):
            os.makedirs(index_dir)
            print(f"Created directory {index_dir}")
            print("Index Directory Created Please Place Existing Index file in it")
        print("Index Directory Found.")
        input("Press Enter to Continue...")
    return index_dir


def pdf_files_list(pdf_dir):
    # Function to create a dictionary of PDF files in the directory
    pdf_files_list = {}
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            pdf_files_list[os.path.splitext(file)[0]] = os.path.join(pdf_dir, file)
    return pdf_files_list


# def pdf_index_list(index_dir):
#    if os.path.exists(index_dir):
# CODE FOR PARSING EXISTING Index FILE
# index_pdf_list = ???
#    return index_pdf_list()


def get_index(pdf_dir, pdf_files_list, index_pdf_list):
    # Function to get the index of words from PDF files
    new_pdf_files_list = [file for file in pdf_files_list if file not in index_pdf_list]
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(parse_pdf_files, [os.path.join(pdf_dir, file + '.pdf') for file in new_pdf_files_list])
    raw_index = {}
    for pdf_book, result in results:
        for word, page_nums in result.items():
            # Remove duplicates from page_nums and sort them
            page_nums = sorted(list(set(page_nums)))
            raw_index.setdefault(word, {}).setdefault(pdf_book, []).extend(page_nums)

    # Sort the lines based on the word extracted from each line
    sorted_index = dict(sorted(raw_index.items(), key=lambda item: item[0]))
    return sorted_index


def parse_pdf_files(pdf_dir):
    # Function to parse PDF files and extract words along with their page numbers
    result = {}
    pdf_file_name = os.path.splitext(os.path.basename(pdf_dir))[0]  # Access the first element of the tuple
    try:
        with open(pdf_dir, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                if text:
                    words = text.lower().split()
                    for word in words:
                        word = word.strip(string.punctuation)
                        result.setdefault(word, []).append(page_num + 1)
    except Exception as e:
        print(f"Error processing {pdf_file_name}: {e}")
        return pdf_file_name, None  # Return None for the result instead of recursively calling parse_pdf_files
    return pdf_file_name, result  # Return the result


def final_index_file(index_dir, index, pdf_files_list):
    # Function to write the final index to a file
    file_path = os.path.join(index_dir, "final_index.txt")  # Construct file path for the SQL file
    with open(file_path, 'w', encoding='utf-8') as file:  # Open file in write mode
        for word, word_data in index.items():
            for pdf_file_name, page_numbers in word_data.items():
                page_numbers = ','.join(map(str, page_numbers))  # Concatenate page numbers without spaces
                file.write(f"{word}|:|{pdf_file_name.replace("'", "''")}|:|{page_numbers}\n")
    print(f"Index saved to {file_path}")


if __name__ == '__main__':
    print("Welcome to PDF Search Engine!\n")
    pdf_dir = get_pdf_dir()
    index_dir = get_index_dir()
    pdf_files_list = pdf_files_list(pdf_dir)
    pdf_index_list = []  # pdf_index_list(index_dir)
    index = get_index(pdf_dir, pdf_files_list, pdf_index_list)
    final_index_file(index_dir, index, pdf_files_list)

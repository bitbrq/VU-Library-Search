import os
import PyPDF2
import string
from multiprocessing import Pool, cpu_count

def get_pdf_dir():
    # Function to get the directory containing PDF files
    pdf_dir = "Books"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        pdf_dir_msg = f"Created directory {pdf_dir} for placing PDF files"
    else:
        pdf_dir_msg = f"Directory {pdf_dir} already exists. Please add files other then existing in directory {pdf_dir}"
    return pdf_dir, pdf_dir_msg

def get_index_dir():
    # Function to get the directory containing the Index file
    index_dir = "Index"
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
        index_dir_msg = f"Created directory {index_dir} for placing index file"
    else:
        index_dir_msg = f"Directory {index_dir} already exists."
    return index_dir, index_dir_msg


def pdf_files_list(pdf_dir):
    # Function to create a dictionary of PDF files in the directory
    pdf_files_list = {}
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            pdf_files_list[os.path.splitext(file)[0]] = os.path.join(pdf_dir, file)
    return pdf_files_list


def index_files_list(index_dir):
    index_files_list = {}
    if os.path.exists(index_dir):
        file_path = os.path.join(index_dir, "final_index.txt")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split("|:|")
                    if len(parts) >= 2:
                        pdf_name = parts[1].strip()
                        index_files_list[pdf_name] = True
    return index_files_list


def get_index(pdf_dir, pdf_files_list, index_files_list):
    # Function to get the index of words from PDF files
    new_pdf_files_list = [file for file in pdf_files_list if file not in index_files_list]
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(parse_pdf_files, [os.path.join(pdf_dir, file + '.pdf') for file in new_pdf_files_list])
    index = {}
    if len(results)>1:
        for pdf_book, result in results:
            for word, page_nums in result.items():
                # Remove duplicates from page_nums and sort them
                page_nums = sorted(list(set(page_nums)))
                index.setdefault(word, {}).setdefault(pdf_book, []).extend(page_nums)
    return index


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
        print(f"An unexpected error occurred while parsing PDF file '{pdf_dir}': {e}")
    return result

def final_index_file(index_dir, index):
    # Function to write the final index to a file
    file_path = os.path.join(index_dir, "final_index.txt")  # Construct file path for the index file
    with open(file_path, 'a', encoding='utf-8') as file:  # Open file in append mode
        for word, word_data in index.items():
            for pdf_file_name, page_numbers in word_data.items():
                page_numbers = ','.join(map(str, page_numbers))  # Concatenate page numbers without spaces
                file.write(f"{word}|:|{pdf_file_name.replace("'", "''")}|:|{page_numbers}\n")


def index_file_sort(index_dir, index_files_list):
    file_path = os.path.join(index_dir, "final_index.txt")
    if index_files_list is not None:
        with open(file_path, "r", encoding='utf-8') as file:
            lines = file.readlines()
        lines.sort()  # Sort the lines
        with open(file_path, "w", encoding='utf-8') as file:
            file.writelines(lines)




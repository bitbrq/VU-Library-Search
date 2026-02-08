import os
import PyPDF2
import string
from multiprocessing import Pool, cpu_count


def get_pdf_dir():
    # Directory containing PDF files
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


def get_db_dir():
    # Directory containing Database file
    print("Default Path for Database file is '/Database'.")
    user_selection = input("Would you like to change path for Database File? Press 'y' for yes, or 'n' for no. : ")
    if user_selection == 'y':
        db_dir = input("Press Enter your Directory Address Where Database File is Located...")
    else:
        db_dir = "Database"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"Created directory {db_dir}")
            print("Database Directory Created Please Place Existing Database file in it")
        print("Database Directory Found.")
        input("Press Enter to Continue...")
    return db_dir


def pdf_files_list(pdf_dir):
    pdf_files_list = {}
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            pdf_files_list[os.path.splitext(file)[0]] = os.path.join(pdf_dir, file)
    return pdf_files_list


#def pdf_db_list(db_dir):
#    if os.path.exists(db_dir):
        # CODE FOR PARSING EXISTING DATABASE FILE
        #db_pdf_list = ???
#    return db_pdf_list()


def get_index(pdf_dir, pdf_files_list, db_pdf_list):
    new_pdf_files_list = [file for file in pdf_files_list if file not in db_pdf_list]
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


def final_db_file(db_dir, index, pdf_files_list):
    file_path = os.path.join(db_dir, "index.sql")  # Construct file path for the SQL file
    with open(file_path, 'w', encoding='utf-8') as file:  # Open file in write mode
        file.write("-- phpMyAdmin SQL Dump\n")
        file.write("-- version 5.2.1\n")
        file.write("-- https://www.phpmyadmin.net/\n")
        file.write("--\n")
        file.write("-- Host: 127.0.0.1\n")
        file.write("-- Generation Time: Dec 02, 2023 at 07:22 PM\n")
        file.write("-- Server version: 10.4.28-MariaDB\n")
        file.write("-- PHP Version: 8.2.4\n")
        file.write("\n")
        file.write("SET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";\n")
        file.write("START TRANSACTION;\n")
        file.write("SET time_zone = \"+00:00\";\n")
        file.write("\n")
        file.write("/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n")
        file.write("/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;\n")
        file.write("/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;\n")
        file.write("/*!40101 SET NAMES utf8mb4 */;\n")
        file.write("\n")
        file.write("--\n")
        file.write("-- Database: `index_db`\n")
        file.write("--\n")
        file.write("\n")
        file.write("-- --------------------------------------------------------\n")
        file.write("\n")
        file.write("-- Table structure for table `pdf_files`\n")
        file.write("--\n")
        file.write("\n")
        file.write("CREATE TABLE IF NOT EXISTS `pdf_files` (\n")
        file.write("  `ID` bigint(20) NOT NULL AUTO_INCREMENT,\n")
        file.write("  `pdf_name` text NOT NULL,\n")
        file.write("  PRIMARY KEY (`ID`)\n")
        file.write(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;\n")
        file.write("\n")
        file.write("-- Dumping data for table `pdf_files`\n")
        file.write("--\n")
        file.write("\n")
        for pdf_file_name in pdf_files_list:
            file.write(f"INSERT INTO `pdf_files` (`pdf_name`) VALUES ('{pdf_file_name}');\n")
        file.write("\n")
        file.write("-- --------------------------------------------------------\n")
        file.write("\n")
        file.write("-- Table structure for table `word_index`\n")
        file.write("--\n")
        file.write("\n")
        file.write("CREATE TABLE IF NOT EXISTS `word_index` (\n")
        file.write("  `ID` bigint(20) NOT NULL AUTO_INCREMENT,\n")
        file.write("  `word` text NOT NULL,\n")
        file.write("  `pdf_file_id` bigint(20) NOT NULL,\n")
        file.write("  `page_number` int(11) NOT NULL,\n")
        file.write("  PRIMARY KEY (`ID`),\n")
        file.write("  FOREIGN KEY (`pdf_file_id`) REFERENCES `pdf_files` (`ID`)\n")
        file.write(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;\n")
        file.write("\n")
        file.write("-- Dumping data for table `word_index`\n")
        file.write("--\n")
        file.write("\n")
        for word, word_data in index.items():
            for pdf_file_name, page_numbers in word_data.items():
                page_numbers = ','.join(map(str, page_numbers))  # Concatenate page numbers without spaces
                file.write(
                    f"INSERT INTO `word_index` (`word`, `pdf_file_id`, `page_number`) VALUES ('{word}', '{pdf_file_name.replace("'", "''")}', {page_numbers});\n")

        file.write("\n")
        file.write("COMMIT;\n")
    print(f"Index saved to {file_path}")


if __name__ == '__main__':
    print("Welcome to PDF Search Engine!\n")

    pdf_dir = get_pdf_dir()
    db_dir = get_db_dir()
    pdf_files_list = pdf_files_list(pdf_dir)
    pdf_db_list = [] #pdf_db_list(db_dir)

    index = get_index(pdf_dir, pdf_files_list, pdf_db_list)
    print(index)
    final_db_file(db_dir, index, pdf_files_list)


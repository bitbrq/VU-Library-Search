from script import *
from GUI import *

if __name__ == '__main__':
    print("Welcome to PDF Search Engine!\n")
    pdf_dir, pdf_dir_msg = get_pdf_dir()
    index_dir, index_dir_msg = get_index_dir()
#    pdf_files_list = pdf_files_list(pdf_dir)
#    index_files_list = index_files_list(index_dir)
#    print (index_files_list)
#    index = get_index(pdf_dir, pdf_files_list, index_files_list)
#    final_index_file(index_dir, index)
#    index_file_sort(index_dir, index_files_list)
    create_word_search_app(index_dir)
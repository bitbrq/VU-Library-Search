import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

def create_word_search_app(index_dir):
    def binary_search(file, word):
        low = 0
        high = len(file) - 1
        result_lines = []
        while low <= high:
            mid = (low + high) // 2
            line = file[mid]
            if line.startswith(word):
                result_lines.append(line)
                # Check previous lines for the same word
                left = mid - 1
                while left >= 0 and file[left].startswith(word):
                    result_lines.append(file[left])
                    left -= 1
                # Check following lines for the same word
                right = mid + 1
                while right < len(file) and file[right].startswith(word):
                    result_lines.append(file[right])
                    right += 1
                return result_lines
            elif word < line.split()[0]:
                high = mid - 1
            else:
                low = mid + 1
        return result_lines

    def search_word(event=None):  # Add event=None for Enter key event
        word = entry.get().strip()
        if not word:
            messagebox.showinfo("Error", "Please enter a word to search for.")
            return
        result = binary_search(lines, word)
        output.delete(1.0, tk.END)  # Clear previous results
        if result:
            for line in result:
                output.insert(tk.END, line)
        else:
            output.insert(tk.END, "Word not found.")

    # Create the main window
    window = tk.Tk()
    window.title("Word Search")

    # Read lines from file
    file_path = os.path.join(index_dir, "final_index.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()  # Read all lines into memory

    # Create frame for search bar and button
    frame = tk.Frame(window)
    frame.pack(fill=tk.X, padx=10, pady=10)

    # Create input field
    entry = tk.Entry(frame)
    entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
    entry.bind("<Return>", search_word)  # Bind Enter key to search_word function

    # Create search button
    search_button = tk.Button(frame, text="Search", command=search_word)
    search_button.pack(side=tk.LEFT)

    # Create output text area
    output = scrolledtext.ScrolledText(window, width=150, height=75)
    output.pack(pady=10)

    # Run the Tkinter event loop
    window.mainloop()

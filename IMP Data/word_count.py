from collections import Counter

if __name__ == '__main__':
    # Initialize a Counter for word counts
    words_to_count = Counter()

    # Open the text file for reading with explicit encoding
    with open("demofile2.txt", "r", encoding="utf-8") as data:
        # Iterate through each line in the file
        for line in data:
            # Tokenize words by splitting the line
            words = line.split()

            # Update the word counts
            words_to_count.update(words)

    # Open a text file for writing the counts
    with open("word_count.txt", "a", encoding="utf-8") as f:
        # Write the counts to the output file
        for word, count in words_to_count.items():
            f.write(f"{word}: {count}\n")

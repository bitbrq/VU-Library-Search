if __name__ == '__main__':
    # Initialize variables for each alphabet letter, digit, and symbol
    characters_to_count = {chr(i): 0 for i in range(32, 127)}

    # Open the text file for reading with explicit encoding
    with open("demofile2.txt", "r", encoding="utf-8") as data:
        # Iterate through each line in the file
        for line in data:
            # Iterate through each character in the line
            for char in line:
                # Check if the character is a printable ASCII character
                if 32 <= ord(char) < 127:
                    # Increment the count for the respective character
                    characters_to_count[char] += 1

    # Open a text file for writing the counts
    with open("char_count.txt", "a", encoding="utf-8") as f:
        # Write the counts to the output file
        for char, count in characters_to_count.items():
            f.write(f"{char}: {count}\n")

        total_count = sum(characters_to_count.values())
        f.write(f"Total Characters: {total_count}\n")
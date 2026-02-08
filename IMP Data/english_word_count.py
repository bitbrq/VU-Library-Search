from collections import Counter
import nltk
from nltk.corpus import words

nltk.download('words')

english_word_set = set(words.words())

def is_english(word):
    return word.lower() in english_word_set

if __name__ == '__main__':
    # Initialize a Counter for English word counts
    english_words_to_count = Counter()

    # Open the text file for reading with explicit encoding
    with open("word_count.txt", "r", encoding="utf-8") as data:
        # Tokenize words using nltk
        words = nltk.word_tokenize(data.read())

        # Update the English word counts
        english_words = [word.lower() for word in words if is_english(word)]
        english_words_to_count.update(english_words)

    # Open a text file for writing the counts of English words
    with open("english_word_count.txt", "w", encoding="utf-8") as f:
        # Write the counts to the output file
        for word, count in english_words_to_count.items():
            f.write(f"{word}: {count}\n")

import random
import csv
import nltk
from nltk.corpus import words, brown

nltk.download("words")
nltk.download("brown")

brown_words = set()
for w in brown.words():
    if w.isalpha() and w.islower():
        brown_words.add(w.lower())

common_word_list = []
for word in words.words():
    if word.lower() in brown_words and 4 <= len(word) <= 6 and word.islower():
        common_word_list.append(word)

unique_words = random.sample(common_word_list, 1000)

output_path = "words.csv"
with open(output_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Words"])
    for word in unique_words:
        writer.writerow([word])

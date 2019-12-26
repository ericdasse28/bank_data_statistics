import pandas as pd
from collections import Counter


# There are columns representing dates. We must indicate them when creating
# the dataframe using the parse_dates argument
data = pd.read_csv("data/operations.csv", parse_dates=[1, 2])
print(data)


# Creating a function to retrieve the most frequent words within the 'libelle'
# column to better track consumption habits
def most_common_words(labels):
    words = []
    for lab in labels:
        words += lab.split(" ")

    counter = Counter(words)
    for word in counter.most_common(100):
        print(word)

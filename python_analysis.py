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


most_common_words(data["libelle"].values)

# After executing the code below, we notice that the word 'CARTE' appears 247
# times. By looking at the data matrix, we understand that this corresponds
# to credit card operations. We will call this the 'type' of the operation

# Also, we notice 16 occurrences of the word 'CHEZ' as well 16 of the word 'LUC'
# which corresponds actually to the restaurant name 'CHEZ LUC'. In other words,
# the owner of that account used his/her credit card 16 times to pay a bill at
# that restaurant. We will call the restaurant the 'category' of the operation

# Stemming from this, we can create two variables TYPE and CATEG
CATEG = {
    'LOYER' : 'LOYER',
    'FORFAIT COMPTE SUPERBANK' : 'COTISATION BANCAIRE',
    'LES ANCIENS ROBINSONS' : 'COURSES',
    "L'EPICERIE DEMBAS" : 'COURSES',
    'TELEPHONE' : 'FACTURE TELEPHONE',
    'LA CCNCF' : 'TRANSPORT',
    'CHEZ LUC' : 'RESTAURANT',
    'RAPT' : 'TRANSPORT',
    'TOUPTIPRI' : 'COURSES',
    'LA LOUVE' : 'COURSES',
    'VELOC' : 'TRANSPORT'
}
TYPE = {
    'CARTE' : 'CARTE',
    'VIR' : 'VIREMENT',
    'VIREMENT' : 'VIREMENT',
    'RETRAIT' : 'RETRAIT',
    'PRLV' : 'PRELEVEMENT',
    'DON' : 'DON'
}

EXPENSES = [80, 120]  # Expense categories boundaries: small, average, big
LAST_BALANCE = 2400  # Last known balance
WEEKEND = ["Saturday", "Sunday"]  # Non-working days

# Here, it's assumed that a small expense is below 80€, an average one between
# 80€ and 120€ and finally, a big one over 120€

# The LAST_BALANCE constant corresponds to the balance of the account after the
# last operation in our csv file


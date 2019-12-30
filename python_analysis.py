import matplotlib.pyplot as plt
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


# Column check
for c in ['date_operation', 'libelle', 'debit', 'credit']:
    if c not in data.columns:
        if (c in ['debit', 'credit'] and 'montant' not in data.columns) or \
                (c not in ['debit', 'credit']):
            msg = "You are missing the column {}. Pay attention to upper "
            msg += "and lower case characters in the column names"
            raise Exception(msg.format(c))

# Deleting worthless columns
for c in data.columns:
    if c not in ['date_operation', 'libelle', 'debit', 'credit', 'montant']:
        del data[c]

# Adding the 'montant' column
if 'montant' not in data.columns:
    data["debit"] = data["debit"].fillna(0)
    data["credit"] = data["credit"].fillna(0)
    data["montant"] = data["debit"] + data["credit"]
    del data["debit"], data["credit"]

# Creation of the 'solde_avt_ope' variable
data = data.sort_values("date_operation")
amount = data["montant"]
balance = amount.cumsum()
balance = list(balance.values)
last_val = balance[-1]
balance = [0] + balance[:-1]
balance = balance - last_val + LAST_BALANCE
data["solde_avt_ope"] = balance


# Assigning operations to a category and a type
def detect_words(values, dictionary):
    result = []
    for lib in values:
        operation_type = "OTHER"
        for word, val in dictionary.items():
            if word in lib:
                operation_type = val
        result.append(operation_type)

    return result


data["categ"] = detect_words(data["libelle"], CATEG)
data["type"] = detect_words(data["libelle"], TYPE)


# Creation of the columns 'tranche_depense' and 'sens'
def expense_slice(value):
    value = value  # Expenses are negative numbers
    if value < 0:
        return "(not an expense)"
    elif value < EXPENSES[0]:
        return "small"
    elif value < EXPENSES[1]:
        return "average"
    else:
        return "big"


data["tranche_depense"] = data["montant"].map(expense_slice)
data["sens"] = ["credit" if m > 0 else "debit" for m in data["montant"]]


# Creation of the other variables
data["annee"] = data["date_operation"].map(lambda d: d.year)
data["mois"] = data["date_operation"].map(lambda d: d.month)
data["jour"] = data["date_operation"].map(lambda d: d.day)
data["jour_sem"] = data["date_operation"].map(lambda d: d.day_name())
data["jour_sem_num"] = data["date_operation"].map(lambda d: d.weekday()+1)
data["weekend"] = data["jour_sem"].isin(WEEKEND)
data["quart_mois"] = [int((jour - 1)*4/31)+1 for jour in data["jour"]]


# QUANTITATIVE VARIABLE
# Pie chart
data["categ"].value_counts(normalize=True).plot(kind='pie')

# This line makes sure the pie chart is a circle instead of an ellipse
plt.axis('equal')
plt.show()

# Bar graph (diagramme en tuyaux d'orgue)
data["categ"].value_counts(normalize=True).plot(kind='bar')
plt.show()

# QUANTITATIVE VARIABLE
# Bar graph (diagramme en bâtons)
data["quart_mois"].value_counts(normalize=True).plot(kind='bar', width=0.1)
plt.show()

# Histogram
data["montant"].hist(density=True)
plt.show()

# A prettier version of the histogram
data[data.montant.abs < 100]["montant"].hist(density=True, bins=20)
plt.show()

# Saving to a CSV file
data.to_csv("data/operations_enrichies.csv", index=False)

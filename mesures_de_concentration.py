import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("data/operations_enrichies.csv", parse_dates=[0])

depenses = data[data['montant'] < 0]
dep = -depenses['montant'].values
n = len(dep)
lorenz = np.cumsum(np.sort(dep)) / dep.sum()
lorenz = np.append([0], lorenz)  # La courbe de Lorenz commence à 0

plt.axes().axis('equal')
xaxis = np.linspace(0-1/n,1+1/n,n+1)  # Il y a un segment de taille n pour
# chaque individu, plus 1 segment supplémentaire d'ordonnée 0. Le premier
# commence à 0-1/n, et le dernier commence à 1+1/n.
plt.plot(xaxis, lorenz, drawstyle="steps-post")
plt.show()

from docplex.mp.model import Model
import numpy as np


filename = 'CM_n=40_m=7.txt'
with open(filename, 'r') as file:
    n = int(filename.split('_')[1].split('=')[1])
    m = int(filename.split('_')[2].split('=')[1].split('.')[0])
    CM = []

    for line in file.readlines():
        CM.extend([int(x) for x in line.split()])
    #print(CM)
file.close()

CM = np.array(CM).reshape(n*m, n*m)
#print(CM)
chunks = []
for i in range(0, n*m, m):
    for j in range(0, n*m, m):
        chunk = CM[i:i+m, j:j+m]
        chunks.append(chunk)
#print(chunks)
# Inicjalizacja modelu
model = Model()

# Zmienne decyzyjne
x = model.binary_var_matrix(range(1, n + 1), range(1, m + 1))
model.minimize(1)

# Ograniczenia

for i in range(1, n + 1):
    model.add_constraint(model.sum(x[i, j] for j in range(1, m + 1)) == 1)

for i in range(n):      # Iteracja po samolotach
    for j in range(m):      # Iteracja po manewrach dla samolotu
        for k in range(i + 1, n):       # Iteracja po innych samolotach - tylko gorny trojkat macierzy
            if i != k:      # Unikamy porównania samolotu z samym sobą
                for l in range(m):      # Iteracja po manewrach dla samolotu k
                    # Sprawdzenie, czy istnieje konflikt między manewrem j samolotu i oraz manewrem l samolotu k
                    chunk = chunks[i*n+k]
                    if chunk[j][l] == 1:
                        # Dodanie ograniczenia do modelu
                        model.add_constraint(x[i+1, j+1]+x[k+1, l+1] <= 1)

# Rozwiązanie problemu
solution = model.solve()

if solution is not None:
    # Wypisanie rozwiązania
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if x[i, j].solution_value == 1:
                print('Samolot {0} wykonuje manewr {1}'.format(i, j))
else:
    print('Nie znaleziono rozwiązania.')
import random
import numpy as np
from docplex.mp.model import Model
import time
import matplotlib.pyplot as plt

def generate_random_instance(n, m, w, p):
    CM = [[0] * (n * m) for _ in range(n * m)]
    indices = [(i, j) for i in range(n * m) for j in range(i + 1, n * m) if (i // m) != (j // m)]
    ones = random.sample(indices, int(w*len(indices)))
    for i, j in ones:
        CM[i][j] = 1
        CM[j][i] = 1
    return CM


def read_file(filename):
    with open(filename, 'r') as file:
        n = int(filename.split('_')[1].split('=')[1])
        m = int(filename.split('_')[2].split('=')[1].split('.')[0])
        CM = [int(x) for line in file for x in line.split()]
    return n, m, np.array(CM).reshape(n*m, n*m)

def create_chunks(CM, n, m):
    chunks = []
    for i in range(0, n*m, m):
        for j in range(0, n*m, m):
            chunk = CM[i:i+m, j:j+m]
            chunks.append(chunk)
    return chunks

def create_model_opt(n, m):
    model = Model()
    model.name = 'Model_optymalny'
    x = model.binary_var_matrix(range(1, n + 1), range(1, m + 1), name=lambda ns: f'x_{ns[0]}_{ns[1]}')
    model.minimize(model.sum(j * x[i, j] for i in range(1, n + 1) for j in range(1, m + 1)))
    #model.minimize(1)
    return model, x

def create_model_fea(n, m):
    model = Model()
    model.name = 'Model_dopuszczalny'
    x = model.binary_var_matrix(range(1, n + 1), range(1, m + 1), name=lambda ns: f'x_{ns[0]}_{ns[1]}')
    model.minimize(1)
    return model, x

def add_constraints(model, n, m, x, chunks):
    for i in range(1, n + 1):
        model.add_constraint(model.sum(x[i, j] for j in range(1, m + 1)) == 1)

    for i in range(n):
        for j in range(m):
            for k in range(i + 1, n):
                if i != k:
                    for l in range(m):
                        chunk = chunks[i*n+k]
                        if chunk[j][l] == 1:
                            model.add_constraint(x[i+1, j+1]+x[k+1, l+1] <= 1)

def solve_model(model):
    start_time = time.time()
    model.solve()
    stop_time = time.time()
    return stop_time - start_time

def print_solution_opt(model, execution_time):
    if model.solution is not None:
        print(f'Czas wykonania: {execution_time} sekund')
        print(model.solution.display())
    else:
        print(f'Czas wykonania: {execution_time} sekund')
        print('Nie znaleziono rozwiązania optymalnego.')

def print_solution_fea(model, execution_time):
    if model.solution is not None:
        print(f'Czas wykonania: {execution_time} sekund')
        print(model.solution.display())
    else:
        print(f'Czas wykonania: {execution_time} sekund')
        print('Nie znaleziono rozwiązania dopuszczalnego.')

def main():
    n = 10
    m = 3
    w = 1
    p = 0.5
    CM = generate_random_instance(n, m, w, p)
    with open(f'CM_n={n}_m={m}.txt', 'w') as file:
        for row in CM:
            file.write(' '.join(str(x) for x in row) + '\n')
    
    chunks = create_chunks(CM, n, m)
    model, x = create_model_fea(n, m)
    add_constraints(model, n, m, x, chunks)
    execution_time = solve_model(model)
    print_solution_fea(model, execution_time)
    model.clear()

    model, x = create_model_opt(n, m)
    add_constraints(model, n, m, x, chunks)
    execution_time = solve_model(model)
    print_solution_opt(model, execution_time)


if __name__ == '__main__':
    main()
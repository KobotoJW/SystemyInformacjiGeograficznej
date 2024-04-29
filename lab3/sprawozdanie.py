import random
import numpy as np
from docplex.mp.model import Model
import time
import matplotlib.pyplot as plt

def generate_conflict_matrix(n, m, w, p):
    pm = p * 2**((1-m)/w)
    rows = n * m
    conflicts_num = int(((rows - 1) * rows * pm) / 2)
    
    matrix = np.zeros((rows, rows), dtype=int)
    indices = random.sample(range(rows * (rows - 1) // 2), conflicts_num)
    indices_set = set(indices)
    k = 0
    for i in range(rows - 1):
        for j in range(i + 1, rows):
            if k in indices_set:
                matrix[i, j] = 1
                matrix[j, i] = 1
            k += 1
    np.fill_diagonal(matrix, 1)
    return matrix


# def read_file(filename):
#     with open(filename, 'r') as file:
#         n = int(filename.split('_')[1].split('=')[1])
#         m = int(filename.split('_')[2].split('=')[1].split('.')[0])
#         CM = [int(x) for line in file for x in line.split()]
#     return n, m, np.array(CM).reshape(n*m, n*m)

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

def analyze_parameters():
    n_values = [10, 20, 30, 40]
    m_values = [3, 5, 7, 9]
    p_values = [0.6, 0.8, 1]
    w_values = [1, 5, 10]
    results = []

    for n in n_values:
        print(f'n = {n}')
        for m in m_values:
            print(f'm = {m}')
            for p in p_values:
                print(f'p = {p}')
                for w in w_values:
                    print(f'w = {w}')
                    for i in range(10): 
                        print(f'Iteracja {i}')
                        CM = generate_conflict_matrix(n, m, w, p)
                        chunks = create_chunks(CM, n, m)

                        start_time = time.time()
                        model, x = create_model_fea(n, m)
                        add_constraints(model, n, m, x, chunks)
                        solve_model(model)
                        execution_time_fea = time.time() - start_time
                        if model.solution is None:
                            solution_fea_exists = False
                        else:
                            solution_fea_exists = True
                        model.clear()

                        start_time = time.time()
                        model, x = create_model_opt(n, m)
                        add_constraints(model, n, m, x, chunks)
                        solve_model(model)
                        execution_time_opt = time.time() - start_time
                        if model.solution is None:
                            solution_opt_exists = False
                        else:
                            solution_opt_exists = True
                        model.clear()

                        results.append((n, m, p, w, execution_time_fea, solution_fea_exists, execution_time_opt, solution_opt_exists))

    return results

def main():
    results = analyze_parameters()
    with open('results2.txt', 'w') as file:
        for result in results:
            file.write(f'{result}\n')


if __name__ == '__main__':
    main()
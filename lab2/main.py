from docplex.mp.model import Model
from cplex.exceptions import CplexError, CplexSolverError
import numpy as np
import time

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

def create_model(n, m):
    model = Model()
    model.name = 'Model_2'
    x = model.binary_var_matrix(range(1, n + 1), range(1, m + 1), name=lambda ns: f'x_{ns[0]}_{ns[1]}')
    model.minimize(model.sum(j * x[i, j] for i in range(1, n + 1) for j in range(1, m + 1)))
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

def print_solution(model, execution_time):
    if model.solution is not None:
        print(f'Czas wykonania: {execution_time} sekund')
        print(model.solution.display())
    else:
        print('Nie znaleziono rozwiązania.')

def main():
    tries = 50
    filenames = ['CM_n=10_m=7.txt', 'CM_n=20_m=7.txt', 'CM_n=30_m=7.txt', 'CM_n=40_m=7.txt']
    for filename in filenames:
        print(f'Processing file: {filename}')
        n, m, CM = read_file(filename)
        chunks = create_chunks(CM, n, m)
        model, x = create_model(n, m)
        add_constraints(model, n, m, x, chunks)

        total_time = 0
        for _ in range(tries):
            solution = solve_model(model)
            total_time +=  solution

        average_time = total_time / tries
        print(f'Average execution time for {filename}: {average_time} seconds')
        model.solution.display()
        model.solution.clear()

if __name__ == "__main__":
    main()
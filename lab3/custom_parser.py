import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class Record:
    def __init__(self, n, m, p, w):
        self.n = n
        self.m = m
        self.p = p
        self.w = w
        self.total_5th = 0
        self.total_7th = 0
        self.count_5th = 0
        self.count_7th = 0
        self.count_true = 0
        self.count_total = 0

    def add_data(self, value_5th, value_6th, value_7th, value_8th):
        self.count_total += 1
        if value_6th:
            self.total_5th += value_5th
            self.count_5th += 1
        if value_8th:
            self.total_7th += value_7th
            self.count_7th += 1
        if value_6th or value_8th:
            self.count_true += 1

    def get_average_5th(self):
        return self.total_5th / self.count_5th if self.count_5th else 0

    def get_average_7th(self):
        return self.total_7th / self.count_7th if self.count_7th else 0

    def get_percentage_true(self):
        return self.count_true / self.count_total * 100

def parse_file(filename):
    records = {}
    with open(filename, 'r') as file:
        for row in file.readlines():
            row = row.split("()")
            n, m, p, w, value_5th, value_6th, value_7th, value_8th = eval(row[0])
            key = (n, m, p, w)
            if key not in records:
                records[key] = Record(n, m, p, w)
            records[key].add_data(value_5th, value_6th, value_7th, value_8th)
    return list(records.values())

def print_parsed(records):
    for record in records:
        print(f'n = {record.n}, m = {record.m}, p = {record.p}, w = {record.w}')
        print(f'Średni czas wykonania dla rozwiązania dopuszczalnego: {record.get_average_5th()} sekund')
        print(f'Średni czas wykonania dla rozwiązania optymalnego: {record.get_average_7th()} sekund')
        print(f'Procent poprawnych rozwiązań: {record.get_percentage_true()}%')
    
def main():
    records = parse_file('results3.txt')
    records = [r for r in records if r.w == 1 and r.m == 9]  # Filter records based on w
    n_values = sorted(set(r.n for r in records))  # Extract unique n values

    fig, ax = plt.subplots(figsize=(16, 8))

    colors = cm.rainbow(np.linspace(0, 1, len(n_values)))  # Create a color for each n value

    # Plot for average times
    for n, color in zip(n_values, colors):
        records_n = [r for r in records if r.n == n]  # Filter records for this n value
        p_values = [r.p for r in records_n]
        avg_5th_times = [r.get_average_5th() for r in records_n]
        avg_7th_times = [r.get_average_7th() for r in records_n]

        ax.plot(p_values, avg_5th_times, 'o-', color=color, label=f'Avg feasible time, n={n}')
        ax.plot(p_values, avg_7th_times, 'o--', color=color, label=f'Avg optimal time, n={n}')

    ax.set_xlabel('p')
    ax.set_ylabel('Time (s)')
    ax.set_title('Average times for each p value')
    ax.legend()

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
import matplotlib.pyplot as plt
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
    records = parse_file('results2.txt')
    labels = [f'n={r.n}, m={r.m}, p={r.p}, w={r.w}' for r in records]
    avg_5th_times = [r.get_average_5th() for r in records]
    avg_7th_times = [r.get_average_7th() for r in records]
    percentages = [r.get_percentage_true() for r in records]

    x = np.arange(len(labels))  # the label locations

    fig, axs = plt.subplots(2, 1, figsize=(16, 8))

    # Plot for average times
    axs[0].bar(x - 0.2, avg_5th_times, 0.4, label='Avg feasible time')
    axs[0].bar(x + 0.2, avg_7th_times, 0.4, label='Avg optimal time')

    axs[0].set_ylabel('Time (s)')
    axs[0].set_title('Average times for each parameter set')
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(labels, ha='center', rotation=90, fontsize=6)
    axs[0].legend()

    # Plot for percentage of solutions
    axs[1].bar(x, percentages, 0.4)

    axs[1].set_ylabel('Percentage')
    axs[1].set_title('Percentage of solutions for each parameter set')
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(labels, ha='center', rotation=90, fontsize=6)

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
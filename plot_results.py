import json
import matplotlib.pyplot as plt
import numpy as np


def calc_stats(data_dict):
    num_rows = [int(x) for x in data_dict.keys()]
    num_rows.sort()

    tasks = data_dict.values()[0].keys()
    task_stats = {}

    for task in tasks:
        stats = {}

        for row in num_rows:
            stats[row] = np.array(data_dict[str(row)][task]).mean()

        task_stats[task] = stats

    return task_stats

if __name__ == '__main__':
    with open('results/pandas_benchmark.json', 'r') as f:
        pandas_results = json.load(f)

    with open('results/postgre_benchmark.json', 'r') as f:
        postgre_results = json.load(f)

    pandas_task_stats = calc_stats(pandas_results)
    postgre_task_stats = calc_stats(postgre_results)

    plt.semilogx(
        pandas_task_stats['select'].keys(), pandas_task_stats['select'].values(), 'o')
    plt.semilogx(
        postgre_task_stats['select'].keys(), postgre_task_stats['select'].values(), 'o')
    plt.show()

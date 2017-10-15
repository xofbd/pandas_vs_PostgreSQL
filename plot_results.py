from collections import OrderedDict
import json
import matplotlib.pyplot as plt
import numpy as np


def calc_stats(data_dict):
    num_rows = [int(x) for x in data_dict.keys()]
    num_rows.sort()

    tasks = data_dict.values()[0].keys()
    task_stats = {}

    for task in tasks:
        stats = OrderedDict()

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

    for task in pandas_task_stats.keys():
        x_pandas = pandas_task_stats[task].keys()
        y_pandas = pandas_task_stats[task].values()

        x_postgre = postgre_task_stats[task].keys()
        y_postgre = postgre_task_stats[task].values()

        plt.loglog(x_pandas, y_pandas, '--o', markersize=8, linewidth=2)
        plt.loglog(x_postgre, y_postgre, '--o', markersize=8, linewidth=2)

        plt.xlabel('Number of Rows (-)')
        plt.ylabel('Mean Runtime (seconds)')
        plt.title(task)
        plt.show()

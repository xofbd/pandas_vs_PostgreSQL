from contexttimer import Timer
from postgre_tasks import PostgreTasks


def run_test(csv_file):
    postgre_task = PostgreTasks(csv_file)

    N = 100  # number of test replicates
    tasks = ('load', 'select', 'filter', 'groupby_agg')
    benchmark_dict = {}

    # loop through each task
    for task in tasks:
        print "running " + task + " for " + csv_file
        task_time = []

        for _ in xrange(N):
            with Timer() as t:
                getattr(pandas_task, task)()
                task_time.append(t.elapsed)

        benchmark_dict[task] = task_time

    return benchmark_dict, len()

if __name__ == '__main__':
    import json
    import os

    files = os.listdir('csv')
    result_dict = {}

    for f in files:
        results, row = run_test('csv/' + f)
        result_dict[str(row)] = results

    # dump dictionary to json
    with open('results/postgre_benchmark.json', 'w') as f:
        json.dump(result_dict, f)

from contexttimer import Timer
from pandas_tasks import PandasTasks
from postgre_tasks import PostgreTasks


def run_test(tool, csv_file):

    # define tool to use
    if tool.lower() == 'pandas':
        tool_task = PandasTasks(csv_file)
    elif tool.lower() == 'postgre' or tool.lower() == 'postgresql':
        tool_task = PostgreTasks(csv_file)
    else:
        raise ValueError("tool must either be pandas or postgre")

    N = 10  # number of test replicates
    tasks = ('load', 'select', 'filter', 'groupby_agg')
    benchmark_dict = {}

    # loop through each task
    for task in tasks:
        print "running " + task + " for " + csv_file + " using " + tool
        task_time = []

        for _ in xrange(N):
            with Timer() as t:
                getattr(tool_task, task)()
                task_time.append(t.elapsed)

        benchmark_dict[task] = task_time

    return benchmark_dict, tool_task.get_num_rows()

if __name__ == '__main__':
    import json
    import os
    import sys

    # check input
    if sys.argv[1].lower() == 'pandas':
        tool = 'pandas'
    elif sys.argv[1].lower() == 'postgre' or sys.argv.lower() == 'postgresql':
        tool = 'postgre'
    else:
        raise ValueError("tool must either be pandas or postgre")

    files = os.listdir('csv')
    result_dict = {}

    for f in files:
        results, row = run_test(tool, 'csv/' + f)
        result_dict[str(row)] = results

    # dump dictionary to json
    with open('results/' + tool + '_benchmark.json', 'w') as f:
        json.dump(result_dict, f)

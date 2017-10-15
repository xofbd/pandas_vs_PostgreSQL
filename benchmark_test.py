from contexttimer import Timer
from pandas_tasks import PandasTasks
from postgre_tasks import PostgreTasks


def run_test(tool, csv_file, N=10):
    """Return dictionary of benchmark results and number of rows in the dataset.


    Positional arguments:
        tool: tool to use for benchmark (pandas or postgre)
        csv_file: csv file to use for DataFrame/table creation

    Keyword arguments:
        N: number of test replicates
    """

    # define tool to use
    if tool.lower() == 'pandas':
        tool_task = PandasTasks(csv_file)
    elif tool.lower() == 'postgre' or tool.lower() == 'postgresql':
        tool_task = PostgreTasks(csv_file)
    else:
        raise ValueError("tool must either be pandas or postgre")

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

    num_rows = tool_task.get_num_rows()
    tool_task.clean_up()

    return benchmark_dict, num_rows

if __name__ == '__main__':
    import json
    import os
    import sys

    tool = sys.argv[1].lower()
    num_replicates = sys.argv[2]
    files = os.listdir('csv')
    result_dict = {}

    for f in files:
        results, row = run_test(tool, 'csv/' + f, N=num_replicates)
        result_dict[str(row)] = results

    # dump dictionary to json
    with open('results/' + tool + '_benchmark.json', 'w') as f:
        json.dump(result_dict, f)

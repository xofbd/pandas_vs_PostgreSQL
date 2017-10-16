from contexttimer import Timer
from pandas_tasks import PandasTasks
from postgre_tasks import PostgreTasks


def run_test(tool, csv_file_A, csv_file_B, N=10):
    """Return dictionary of benchmark results and number of rows in the dataset.


    Positional arguments:
        tool: tool to use for benchmark (pandas or postgre)
        csv_file_A: csv file name to use for DataFrame/table A
        csv_file_B: csv file name to use for DataFrame/table B

    Keyword arguments:
        N: number of test replicates
    """

    # define tool to use
    if tool.lower() == 'pandas':
        tool_task = PandasTasks(csv_file_A, csv_file_B)
    elif tool.lower() == 'postgre' or tool.lower() == 'postgresql':
        tool_task = PostgreTasks(csv_file_A, csv_file_B)
    else:
        raise ValueError("tool must either be pandas or postgre")

    # loop through each task
    tasks = ('load', 'select', 'filter', 'groupby_agg', 'join')
    benchmark_dict = {}
    num_rows = tool_task.get_num_rows()

    for task in tasks:
        print "running " + task + " for " + int(num_rows) + " rows "
        " using " + tool
        task_time = []

        for _ in xrange(N):
            with Timer() as t:
                getattr(tool_task, task)()
                task_time.append(t.elapsed)

        benchmark_dict[task] = task_time

    tool_task.clean_up()
    return benchmark_dict, num_rows

if __name__ == '__main__':
    import json
    import os
    import sys

    tool = sys.argv[1].lower()
    num_reps = int(sys.argv[2])
    files_A = os.listdir('csv/A')
    files_B = os.listdir('csv/B')
    result_dict = {}

    for f_A, f_B in zip(files_A, files_B):
        results, row = run_test(
            tool, 'csv/A/' + f_A, 'csv/B/' + f_B, N=num_reps)
        result_dict[str(row)] = results

    # dump dictionary to json
    with open('results/' + tool + '_benchmark.json', 'w') as f:
        json.dump(result_dict, f)

import json


def create_json(results_file):
    tasks = ('load', 'select_', 'filter', 'groupby_agg')
    results_dict = dict(zip(tasks, range(len(tasks))))

    with open(results_file, 'r') as f:
        task = f.readline().strip()

        replicates = []
        results = f.read().split()

        for r in results:
            if r in results_dict.keys():
                results_dict[task] = results
                task = r
                replicates = []
            else:
                replicates.append(float(r) / 1E9)

    # dump dictionary to json
    with open('results.json', 'w') as f:
        json.dump(results_dict, f)


def join_jsons(json_list, dict_keys):
    new_json = {}

    for f, key in zip(json_list, dict_keys):
        new_json[key] = json.load(f)

if __name__ == '__main__':
    import sys

    # for
    create_json(sys.argv[1])

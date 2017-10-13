import json


def create_json(results_file):
    tasks = ('load', 'select', 'filter', 'groupby_agg')
    results_dict = {}

    with open(results_file, 'r') as f:
        task = f.readline().strip()
        results = f.read().split()
        replicates = []

        for r in results:
            if r in tasks:
                results_dict[task] = replicates
                task = r
                replicates = []
            else:
                replicates.append(float(r) / 1E9)

        results_dict[task] = replicates

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
# author: Don Fox
# date: September 30, 2017
# file name: create_dataset.py

import numpy as np
import pandas as pd


def create_csv(n=1000):
    seed = np.random.seed(1)

    columns = ('section', 'score_1', 'score_2')
    labels = ('A', 'B', 'C', 'D')
    letters = np.random.choice(labels, n)
    score_1 = np.random.rand(n)
    score_2 = np.random.rand(n)

    df = pd.DataFrame(dict(zip(columns, [letters, score_1, score_2])))
    df.to_csv('csv/test_' + str(n) + '_rows.csv', index=False)

if __name__ == '__main__':
    import sys

    create_csv(int(sys.argv[1]))

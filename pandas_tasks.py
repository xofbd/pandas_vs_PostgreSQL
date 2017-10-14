# author: Don Fox
# date: September 30, 2017
# file name: pandas_tasks.py

import pandas as pd


class PandasTasks(object):

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = None
        self.columns = ('score_1', 'score_2', 'section')

    def load(self):
        self.df = pd.read_csv(self.csv_file, header=None, index_col=False,
                              names=self.columns)

    def select(self):
        self.df['score_1']

    def filter(self):
        self.df[self.df['section'] == 'A']

    def groupby_agg(self):
        self.df.groupby('section').agg({'score_1': 'mean', 'score_2': 'max'})

    def get_num_rows(self):
        return len(self.df)

    def clean_up(self):
        del(self.df)

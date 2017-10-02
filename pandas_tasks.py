# author: Don Fox
# date: September 30, 2017
# file name: pandas_tasks.py

import pandas as pd


class PandasTasks(object):

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = None

    def load(self):
        self.df = pd.read_csv(self.csv_file)

    def select(self):
        self.df['score 1']

    def filter(self):
        self.df[self.df['section'] == 'A']

    def groupby_agg(self):
        self.df.groupby('section').agg(['mean', 'max'])

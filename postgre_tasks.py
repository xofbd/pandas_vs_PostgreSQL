import psycopg2


class PostgreTasks(object):

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.db = None

    def load(self):
        pass

    def select(self):
        self.curr.execute('SELECT section FROM ')

    def filter(self):
        self.curr.execute('SELECT section FROM WHERE section = A')

    def groupby_agg(self):
        self.curr.execute(
            'SELECT AVG(section), MAX(section) FROM GROUP BY section')

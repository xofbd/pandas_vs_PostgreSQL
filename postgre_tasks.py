import os
import psycopg2


class PostgreTasks(object):

    def __init__(self, csv_file):
        self.csv_file = csv_file

        # get user name for postgre connection
        user = os.popen("echo $USER").read().strip()
        dbname = user

        # create psql connection, cursor, and create test table
        self.conn = psycopg2.connect(dbname=dbname, user=user)
        self.cur = self.conn.cursor()
        self.cur.execute("DROP TABLE IF EXISTS test_table;")

        query = """
        CREATE TABLE test_table
        (score_1 float, score_2 float, section char(1));
        """

        self.cur.execute(query)

    def load(self):
        self.cur.execute("DELETE FROM test_table;")

        with open(self.csv_file, 'r') as f:
            self.cur.copy_from(f, "test_table", sep=',')

    def select(self):
        self.cur.execute('SELECT section FROM test_table;')

    def filter(self):
        self.cur.execute(
            "SELECT section FROM test_table WHERE section = 'A';")

    def groupby_agg(self):
        query = """
        SELECT AVG(score_1), MAX(score_2)
        FROM test_table
        GROUP BY section;
        """

        self.cur.execute(query)

    def get_num_rows(self):
        self.cur.execute("SELECT COUNT(*) FROM test_table;")
        num_rows = self.cur.fetchall()
        return int(num_rows[0][0])

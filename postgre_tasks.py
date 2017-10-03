import psycopg2


class PostgreTasks(object):

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.conn = psycopg2.connect(dbname="dbf", user="dbf")
        self.cur = self.conn.cursor()

        self.cur.execute("DROP TABLE IF EXISTS test_table_2;")

        query = """
        CREATE TABLE test_table_2
        (score_1 float, score_2 float, section char(1));
        """
        self.cur.execute(query)

    def load(self):
        self.cur.execute("DELETE FROM test_table_2;")

        with open(self.csv_file, 'r') as f:
            self.cur.copy_from(f, "test_table_2", sep=',')

    def select(self):
        self.cur.execute('SELECT section FROM test_table_2;')

    def filter(self):
        self.cur.execute(
            "SELECT section FROM test_table_2 WHERE section = 'A';")

    def groupby_agg(self):
        query = """
        SELECT AVG(score_1)
        FROM test_table_2
        GROUP BY section;
        """

        self.cur.execute(query)

    def get_num_rows(self):
        self.cur.execute("SELECT COUNT(*) FROM test_table_2;")
        num_rows = self.cur.fetchall()
        return int(num_rows[0][0])

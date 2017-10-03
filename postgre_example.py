import psycopg2

conn = psycopg2.connect(dbname="dbf", user="dbf")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS test_table;")
conn.commit()
print "pass"

query = """
CREATE TABLE test_table
(score_1 float, score_2 float, section char(1));
"""

print "pass"
cur.execute(query)
# cur.execute("DELETE FROM test;")
# cur.close()
with open("csv/test_10_rows.csv", "r") as f:
    cur.copy_from(f, "test_table", sep=",")

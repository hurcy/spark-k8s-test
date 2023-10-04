# import time
import sys
import psycopg2
import time

from pyspark.sql import SparkSession


spark = (
  SparkSession
    .builder
    # .master("spark://172.22.249.66")
    # .enableHiveSupport()
    .getOrCreate()
)

def get_pg_conn():
  try:
    conn = psycopg2.connect(
        host="172.22.249.59",
        database="cdw",
        port=5432,
        user="spark",
        password="SparkPlusEd!@"
    )
    return conn
  except psycopg2.DatabaseError as db_err:
    print(db_err)


def execute(sql):
  conn = get_pg_conn()
  with conn:
    with conn.cursor() as curs:
      curs.execute(sql)
  conn.close()


if __name__ == "__main__":
  var = sys.argv[1]
  print(f"hello spark{var}!")
  execute(f"insert into dkuh_dm.ed_test values ({var})")
  f = open('file:///test.sql', 'r') 
  sql_text = f.read()
  print(sql_text)
  execute(sql_text)

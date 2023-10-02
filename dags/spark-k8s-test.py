import pendulum

from airflow import DAG
from airflow.settings import TIMEZONE
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator


default_args = {
    "depends_on_past": False
}

with DAG(
    dag_id=f"test_spark_k8s",
    start_date=pendulum.datetime(2023, 9, 26, tz=TIMEZONE),
    schedule_interval="30 0 * * *",
    catchup=False,
    tags=["test"],
    max_active_runs=1,
    default_args=default_args
) as dag:
  pi_test = SparkSubmitOperator(
      application="/opt/airflow/dags/pi.py",
      conn_id="spark_standalone",
      task_id="pi_test",
      conf={
          # "spark.eventLog.enabled": True,
          # "spark.eventLog.dir": "file:///tmp/spark-events",
          "spark.executor.instances": 1,
          "spark.executor.memory": "1g",
          "spark.executor.cores": 1,
          "spark.driver.memory": "1g",
          "spark.driver.cores": 1,
          # "spark.cores.max": 1
      },
      name="pi_test",
      application_args=[10]
  )
  postgres_test = SparkSubmitOperator(
      application="/opt/airflow/dags/spark_app.py",
      conn_id="spark_standalone",
      task_id='postgres_test',
      conf={
          # "spark.eventLog.enabled": True,
          # "spark.eventLog.dir": "file:///tmp/spark-events",
          "spark.executor.instances": 2,
          "spark.executor.memory": "2g",
          "spark.executor.cores": 2,
          "spark.driver.memory": "2g",
          "spark.driver.cores": 2,
          # "spark.cores.max": 2
      },
      application_args=["2"],
      name="postgres_test"
  )

[pi_test, postgres_test]

"""
spark-submit \
  --master <master> \
  pi.py 10
"""

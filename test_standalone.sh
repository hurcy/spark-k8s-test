#!/bin/bash
spark-submit \
    --master spark://spark-master-0.spark-headless.dp-airflow.svc.cluster.local:7077 \
    --name spark-pi \
    dags/pi.py 10

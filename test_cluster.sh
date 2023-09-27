#!/bin/bash
spark-submit \
    --master k8s://https://mgmt-lb-1:6443 \
    --deploy-mode cluster \
    --name spark-pi \
    --conf spark.kubernetes.container.image=greyparrotkhc/spark:3.3.2-hadoop3 \
    dags/pi.py

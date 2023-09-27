import os
import dags_helper

from airflow import DAG
from airflow.configuration import conf

from pipeline_generator.utils.settings import data_layer_dict


data_layer = os.path.dirname(os.path.dirname(__file__)).split("/")[-1]
for dag_info in dags_helper.get_dag_list(data_layer):
  globals()[dag_info.name] = dag_info.dag

globals()[f"{data_layer}_layer_depd_dag"] = dags_helper.get_layer_depd_dag(
    data_layer=data_layer,
    max_active_tasks=data_layer_dict[data_layer].get("max_active_tasks") or conf.getint("core", "max_active_tasks_per_dag"),
    poke_interval=data_layer_dict[data_layer].get("poke_interval") or 60
)

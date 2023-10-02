import dags_helper
import pendulum

from airflow import DAG
from airflow.operators.empty import EmptyOperator
# from airflow.operators.python import PythonOperator
from airflow.settings import TIMEZONE
from airflow.utils.trigger_rule import TriggerRule


from dags_helper.dags_operator import get_trigger_dag_run_operator
# from dags_helper.dags_operator.common import under_maintenance, kill_blocking_process
# from dags_helper.sms_bot import SmsBot
from pipeline_generator.utils.settings import data_layer_dict


default_args = {
    "depends_on_past": False,
    # "on_failure_callback": SmsBot('sms_conn').failure_message
}

with DAG(
    dag_id=f"hrs_dag",
    start_date=pendulum.datetime(2023, 9, 21, tz=TIMEZONE),
    schedule_interval="30 0 * * *",
    catchup=False,
    tags=["hrs_dag"],
    max_active_runs=1,
    default_args=default_args
) as dag:
  hrs_start = EmptyOperator(task_id=f"hrs_start")

  # under_maintenance = PythonOperator(
  #     task_id="under_maintenance",
  #     python_callable=under_maintenance,
  #     op_kwargs={
  #         "minutes": 180
  #     },
  #     provide_context=True
  # )

  # reset_manual_var = PythonOperator(
  #     task_id="reset_manual_var",
  #     python_callable=dags_helper.reset_manual_var,
  # )

  hrs_dag_dict = {
      data_layer: get_trigger_dag_run_operator(
          trigger_dag_id=f"{data_layer}_layer_depd_dag",
          task_id=f"{data_layer}_layer_trigger",
          wait_for_completion=True,
          trigger_rule=getattr(TriggerRule, data_layer_info.get("trigger_rule") or "", TriggerRule.ALL_SUCCESS)
      )
      for data_layer, data_layer_info in data_layer_dict.items()
      if data_layer != "dm"
  }

  # kill_blocking_process = PythonOperator(
  #     task_id="kill_blocking_process",
  #     python_callable=kill_blocking_process,
  #     op_args=[["dw_layer_trigger", "dm_layer_trigger", "odsm_layer_trigger"], 600],
  #     provide_context=True
  # )

  # app_dag = get_trigger_dag_run_operator(
  #     trigger_dag_id="app_layer_dag",
  #     task_id=f"app_layer_trigger",
  #     wait_for_completion=False,
  #     trigger_rule=TriggerRule.ALL_SUCCESS
  # )

  hrs_end = EmptyOperator(
      task_id=f"hrs_end"
      # ,
      # on_success_callback=SmsBot('sms_conn').success_message
  )

  # dependency between layers
  hrs_start >> hrs_dag_dict["dl"] >> hrs_end
  # hrs_start >> under_maintenance >> reset_manual_var >> hrs_dag_dict["bind"] >> hrs_dag_dict["dl"]
  # hrs_dag_dict["dl"] >> [hrs_dag_dict["odsl"], hrs_dag_dict["dw"], hrs_dag_dict["dm"], kill_blocking_process]
  # hrs_dag_dict["odsl"] >> hrs_dag_dict["odsm"]
  # hrs_dag_dict["dw"] >> hrs_end
  # hrs_dag_dict["dm"] >> hrs_end
  # hrs_dag_dict["odsm"] >> hrs_end
  # hrs_end >> app_dag

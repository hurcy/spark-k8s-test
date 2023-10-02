import ast
import pyspark
import sys

from pyspark.sql import SparkSession
from pyspark import StorageLevel
from pyspark_common import (
    match_schema,
    repartition_df,
    spark_start_upd_cdw_log,
    spark_end_upd_cdw_log
)
from jinja2 import Environment

spark = (
    SparkSession
      .builder
      .enableHiveSupport()
      .getOrCreate()
)

vars = {
    "schema": "dl",
    "start_var": sys.argv[1],
    "end_var": sys.argv[2]
}
cluster_manager = "STANDALONE" # OR K8S
resource_type, dag_run_id, conn_dict = sys.argv[3], sys.argv[4], sys.argv[5]
env = Environment()

conn_dict = ast.literal_eval(conn_dict)

spark_start_upd_cdw_log(
    cluster_manager=cluster_manager,
    conn_dict=conn_dict,
    prc_nm="dkuh_dl.s_acpprioe",
    dag_run_id=dag_run_id,
    resource_type=resource_type,
    application_id=spark.sparkContext.applicationId,
    prc_result='SPARK_START'
)
# --


meta_sql = """
select
    table_name,
    array_to_string(
        array_agg(x.column_name || ' ' || 
            case
                when x.data_type = 'character varying' then
                    'varchar'
                when x.data_type = 'timestamp without time zone' then
                    'timestamp'
                when x.data_type = 'timestamp with time zone' then
                    'timestamp'
                else
                    x.data_type
                end || 
            case 
                when x.data_length is not null then
                    '(' || x.data_length || ')'
                else
                    ''
            end
        ), 
        ', '
    ) as column_info
from (
    select
        table_name,
        column_name,
        data_type,
        case 
            when data_type like 'character%' then
                cast(character_maximum_length as text)
            when data_type = 'numeric' then
                case when ( numeric_scale is not null and numeric_scale > 0 ) then
                    cast(numeric_precision as text) || ',' || cast(numeric_scale as text)
                else
                    cast(numeric_precision as text)
                end
            else
                null
        end as data_length
    from
        information_schema.columns
    where
        1=1
        and(table_schema='dkuh_dl' and lower(table_name)='s_acpprioe')
) x
group by
    table_name
"""

df_meta = (
  spark
    .read
    .format("jdbc")
    .option("driver", conn_dict["hrs_conn"]["driver"])
    .option("url", conn_dict["hrs_conn"]["url"])
    .option("user", conn_dict["hrs_conn"]["user"])
    .option("password", conn_dict["hrs_conn"]["password"])
    .option("query", meta_sql)
    .load()
)

assert df_meta.count() == 1, "check if the postgres table is created to retrieve meta data, or whether df_meta has all the information needed, if not fix the meta_sql query"

# step_seq: 1
file = pyspark.SparkFiles.get("full_ext_s_acpprioe.sql")
with open(file) as spark_sql:
  dbtable = "".join(spark_sql.readlines())
dbtable = env.from_string(dbtable).render(**vars)
options = {
    "driver": conn_dict["his_conn"]["driver"],
    "url": conn_dict["his_conn"]["url"],
    "user": conn_dict["his_conn"]["user"],
    "password": conn_dict["his_conn"]["password"],
}

options.update({"dbtable": dbtable})
options.update(
    {
        "sessionInitStatement": """
            BEGIN
                execute immediate 'alter session set NLS_LANGUAGE="KOREAN"';
                execute immediate 'alter session set NLS_TERRITORY="KOREA"';
                execute immediate 'alter session set NLS_DATE_FORMAT="YYYY-MM-DD HH24:MI:SS"';
                execute immediate 'alter session set NLS_TIMESTAMP_FORMAT="YYYY-MM-DD HH24:MI:SSXFF"';
            END;
        """,
        "fetchsize": "1000"
    }
)

df_1 = (
  spark
    .read
    .format("jdbc")
    .options(**options)
    .load()
)
df_1 = repartition_df(spark, df_1)
table_name = "dkuh_dl.s_acpprioe".split(".")[-1]
column_schema = (
  df_meta
    .filter(df_meta.table_name == table_name)
    .select("column_info")
    .first()[0]
)
df_1 = match_schema(column_schema, df_1)
(
  df_1
    .write
    .format("jdbc")
    .option("driver", conn_dict["hrs_conn"]["driver"])
    .option("url", conn_dict["hrs_conn"]["url"])
    .option("dbtable", "dkuh_dl.S_ACPPRIOE")
    .option("user", conn_dict["hrs_conn"]["user"])
    .option("password", conn_dict["hrs_conn"]["password"])
    .mode("append")
    .save()
)

# cdw_log
load_cnt = ""
spark_end_upd_cdw_log(
    cluster_manager=cluster_manager,
    conn_dict=conn_dict,
    prc_nm="dkuh_dl.s_acpprioe",
    dag_run_id=dag_run_id,
    load_cnt=load_cnt,
    prc_result='SPARK_END'
)

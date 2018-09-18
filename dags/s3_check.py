import airflow
from airflow.hooks.S3_hook import S3Hook

s3 = S3Hook('s3_airflow_logs_conn')

s3.load_file(filename='tuto.py',key='logs',bucket_name='airflow-logs-irdeto')
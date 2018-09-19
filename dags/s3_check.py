"""
S3 Sensor Connection Test
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.s3_key_sensor import S3KeySensor
from s3_try import check_it, write_it

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2016, 11, 1),
    'email': ['something@here.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('s3_dag_test', default_args=default_args, schedule_interval='@once')

t1 = BashOperator(
    task_id='bash_test',
    bash_command='echo "hello, it should work"',
    dag=dag)

sensor = S3KeySensor(
    task_id='check_s3_for_file_in_s3',
    bucket_key='logs*',
    wildcard_match=True,
    bucket_name='airflow-logs-ben',
    aws_conn_id='my_conn_S3',
    timeout=18 * 60 * 60,
    poke_interval=120,
    dag=dag)

pythonop = PythonOperator(start_date=datetime(2016, 11, 1), python_callable=check_it, task_id="my_python")
pythonop_write = PythonOperator(start_date=datetime(2016, 11, 1), python_callable=write_it, op_args=["me"],
                                task_id="my_python_write")

t1.set_upstream(sensor)
pythonop.set_upstream(sensor)
pythonop_write.set_upstream(sensor)

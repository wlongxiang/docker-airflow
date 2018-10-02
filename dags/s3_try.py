from airflow.hooks.S3_hook import S3Hook

s3 = S3Hook(aws_conn_id="my_conn_S3")


def check_it():
    f = s3.check_for_bucket("airflow-logs-ben")
    # expect a false return
    return f

def write_it(str_data):
    ret = s3.load_string(string_data=str_data, key="logs/test_write1.txt", bucket_name="airflow-logs-ben")
    return ret


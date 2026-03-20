from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def print_hello():
    print("Hello from Airflow!")
    return "Hello World"

def print_date():
    print(f"Current date: {datetime.now()}")
    return datetime.now()

with DAG(
    'example_dag',
    default_args=default_args,
    description='A simple example DAG',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello,
    )

    task2 = PythonOperator(
        task_id='print_date',
        python_callable=print_date,
    )

    task1 >> task2

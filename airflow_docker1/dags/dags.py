from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

# Hàm để quyết định nhánh
def choose_branch(**kwargs):
    number = int(kwargs['dag_run'].conf.get('number', 0))
    if number < 15:
        return 'task_t2'
    else:
        return 'task_t3'

# Hàm in các số nguyên tố <= number
def print_primes(**kwargs):
    number = int(kwargs['dag_run'].conf.get('number', 0))
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0:
                return False
        return True
    primes = [str(i) for i in range(1, number+1) if is_prime(i)]
    print("Prime numbers <= {}: {}".format(number, ', '.join(primes)))

with DAG(
    dag_id='branching_dag_with_number',
    start_date=datetime(2025, 7, 15),
    schedule=None,
    catchup=False,
) as dag:

    t1 = BranchPythonOperator(
        task_id='decide_path',
        python_callable=choose_branch,
    )

    t2 = BashOperator(
        task_id='task_t2',
        bash_command='echo "Input number is: {{ dag_run.conf["number"] }}"',
    )

    t3 = PythonOperator(
        task_id='task_t3',
        python_callable=print_primes,
    )

    t1 >> [t2, t3]

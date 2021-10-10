""" DAG defining a process to ETL reddit comments
from a predefined list of subreddits. Comments are 
cleaned using spacy and transformed into word vectors
that are loaded into a dynamodb table """

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from dummy_etl import extract_subreddit_comments, transform_directory, load_directory

args = {
    'owner': 'Kevin Nowland',
    'email': 'kevin.nowland@gmail.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'schedule_interval': '@weekly',
    'retries': 0
}

with DAG(
    dag_id='reddit-etl',
    default_args=args,
    start_date=days_ago(2),
    catchup=False
) as dag:

   dir_path = '/home/kevin/Desktop/etl'

    subreddits = [
        'AskHistorians',
        'AskScience'
    ]

    extract_tasks = [
        PythonOperator(
            task_id='extract_' + subreddit,
            python_callable=extract_subreddit_comments,
            op_kwargs={
                'dir_path': dir_path,
                'subreddit': subreddit
            }
        )
        for subreddit in subreddits
    ]

    transform = PythonOperator(
        task_id='transform_raw_datafiles',
        python_callable=transform_directory,
        op_kwargs={'dir_path': dir_path}
    )


    load = PythonOperator(
        task_id='load_into_dynamodb',
        python_callable=load_directory,
        op_kwargs={'dir_path': dir_path}
    )

    # define dag
    for task in extract_tasks:
        task >> transform

    transfrom >> load

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

from plugins.stage_loader import stage_songs_to_postgres, stage_events_to_postgres
from plugins.dq_check import check_table_counts
from sql_queries import *

default_args = {
    'owner' : 'tune_stream',
    'depends_on_past' : False,
    'start_date' : datetime(2025, 7, 15),
    'retries': 3,
    'retry_delay': timedelta(minutes = 5),
    'catchup': False,
    'email_on_retry': False
}

with DAG('tune_stream_etl',
         default_args=default_args,
         description='ETL pipeline for music data',
         schedule='@hourly',
         catchup=False) as dag:

    start_execution = EmptyOperator(task_id='start_execution')

    stage_songs = PythonOperator(
        task_id='stage_songs',
        python_callable=stage_songs_to_postgres
    )

    stage_events = PythonOperator(
        task_id='stage_events',
        python_callable=stage_events_to_postgres
    )

    load_songplays_fact = SQLExecuteQueryOperator(
        task_id='load_songplays_fact',
        conn_id='postgres',
        sql=SqlQueries.songplay_table_insert
    )

    load_user_dim = SQLExecuteQueryOperator(
        task_id='load_user_dim',
        conn_id='postgres',
        sql=SqlQueries.user_table_insert
    )

    load_song_dim = SQLExecuteQueryOperator(
        task_id='load_song_dim',
        conn_id='postgres',
        sql=SqlQueries.song_table_insert
    )

    load_artist_dim = SQLExecuteQueryOperator(
        task_id='load_artist_dim',
        conn_id='postgres',
        sql=SqlQueries.artist_table_insert
    )

    load_time_dim = SQLExecuteQueryOperator(
        task_id='load_time_dim',
        conn_id='postgres',
        sql=SqlQueries.time_table_insert
    )

    run_data_quality_checks = PythonOperator(
        task_id='run_data_quality_checks',
        python_callable=check_table_counts
    )

    end_execution = EmptyOperator(task_id='end_execution')

    # DAG dependencies
    start_execution >> [stage_songs, stage_events] >> load_songplays_fact
    load_songplays_fact >> [load_user_dim, load_song_dim, load_artist_dim, load_time_dim]
    [load_user_dim, load_song_dim, load_artist_dim, load_time_dim] >> run_data_quality_checks
    run_data_quality_checks >> end_execution

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator

dag_params = {
    'dag_id': 'postgres_glints_migration',
    'start_date':datetime(2020, 4, 20),
    'schedule_interval': "@once"
}

def insertToTarget():
    src = PostgresHook(postgres_conn_id='database_x')
    target = PostgresHook(postgres_conn_id='database_y')

    src_conn = src.get_conn()
    cursor = src_conn.cursor()

    cursor.execute("SELECT * FROM sales")
    target.insert_rows(table="sales", rows=cursor)

with DAG(**dag_params) as dag:
    create_pet_table = PostgresOperator(
        task_id="create_sales_table",
        postgres_conn_id="database_y",
        sql="""
            CREATE TABLE IF NOT EXISTS sales (
            id     INTEGER PRIMARY KEY,
            creation_date  VARCHAR(1024),
            sale_value INTEGER);
          """,
    )

    task_load_target = PythonOperator(task_id = 'load_target', python_callable=insertToTarget)

    create_pet_table >> task_load_target
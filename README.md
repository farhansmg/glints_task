# Glints Technical Assessment
Repository of Glints technical assessment

Steps to run it :
* inside this composer includes : 3 postgres service (2 for source and target database and 1 for metadata airflow), redis, airflow_webserver, airflow-scheduler, airflow-worker, first initial airflow, and flower
* container database_x as source db and database_y as target db
* move composer and initial sql DDL files so it could create the table and insert value on it automatically into single directory as shown by the example directory listing below
```
-rw-r--r--  1 farhan farhan 5511 Aug 13 10:21 docker-compose.yml
-rw-rw-r--  1 farhan farhan  537 Aug 13 10:21 docker_postgres_x_init.sql
```
* create 3 directory with this command `mkdir ./dags ./logs ./plugins`
* matching file permission using this command `echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`
* running composer `docker-compose up`
* open localhost:5884 on browser for accessing Apache Airflow webserver, login with credential username : airflow, pass : qwerty1234
* create source postgre connection on `Admin --> Connections --> Add a new record (+) button` with below credential
```
Conn Id : database_x
Conn Type : Postgres
Description : Database Source
Host : localhost
Login : postgres
Password : qwerty
Port : 15432
```
and then click save
* create target postgre connection on `Admin --> Connections --> Add a new record (+) button` with below credential
```
Conn Id : database_y
Conn Type : Postgres
Description : Database Source
Host : localhost
Login : postgres
Password : qwerty1234
Port : 25432
```
and then click save
* move DAG with name `migration.py` into ./dags dir that have been create before
* open localhost:5884 on browser refresh DAGs until you find postgres_glints_migration
* trigger that DAG
* you can validate the result by using your favorite db viewer like navicat / dbeaver / pgadmin


# Setup Setting

Here's the explanation of the setting that I'm using it

* container of source database which is database_x
```yml
  postgres_x:
    container_name: database_x
    image: "postgres:12"
    environment:
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "qwerty"
      PGDATA: "/data/postgres_x"
    volumes:
       - postgres_x:/data/postgres_x
       - ./docker_postgres_x_init.sql:/docker-entrypoint-initdb.d/docker_postgres_x_init.sql
    ports:
      - "15432:5432"
    restart: unless-stopped
```
I'm using DDL entry to automatically create the dummy table and value on it so I don't have to manually insert it to postgre, after that I specify the mapping port to 15432 so I can deploy multiple postgre inside it.

* container of target database which is database_y. It's pretty similiar with container database_x but without DDL entry on it and different port
* container of airflow
```yml
  airflow-webserver:
    <<: *airflow-common
    command: webserver
    ports:
      - 5884:8080
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:5884/health"]
      interval: 10s
      timeout: 10s
      retries: 5
    restart: always

  airflow-scheduler:
    <<: *airflow-common
    command: scheduler
    healthcheck:
      test: ["CMD-SHELL", 'airflow jobs check --job-type SchedulerJob --hostname "$${HOSTNAME}"']
      interval: 10s
      timeout: 10s
      retries: 5
    restart: always

  airflow-worker:
    <<: *airflow-common
    command: celery worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
      interval: 10s
      timeout: 10s
      retries: 5
    restart: always

  airflow-init:
    <<: *airflow-common
    command: version
    environment:
      <<: *airflow-common-env
      _AIRFLOW_DB_UPGRADE: 'true'
      _AIRFLOW_WWW_USER_CREATE: 'true'
      _AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow}
      _AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-qwerty1234}

  flower:
    <<: *airflow-common
    command: celery flower
    ports:
      - 5555:5555
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:5555/"]
      interval: 10s
      timeout: 10s
      retries: 5
    restart: always
```

not to much I modify it, all of it from airflow documentation it self but with port of airflow webserver which the task to change it

* DAG file

```python3
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
    create_sales_table = PostgresOperator(
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

    create_sales_table >> task_load_target
```

For the DAG was pretty much simple because there's no transformation on it just some extract and load it to another database so I'm create first the table to target database and after that I'm select all data from source table into target table.

# Thanks

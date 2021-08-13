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

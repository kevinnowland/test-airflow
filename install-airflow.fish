#!/usr/local/bin/fish

conda activate flow

set -g -x AIRFLOW_HOME ~/airflow
set AIRFLOW_VERSION 2.1.4
set PYTHON_VERSION 3.8
set CONSTRAINT_URL "https://raw.githubusercontent.com/apache/airflow/constraints-$AIRFLOW_VERSION/constraints-$PYTHON_VERSION.txt"

pip install apache-airflow=="$AIRFLOW_VERSION" --constraint "$CONSTRAINT_URL"

airflow db init

airflow users create \
	--username admin \
	--firstname Kevin \
	--lastname Nowland \
	--role Admin \
	--email kevin.nowland@gmail.com

airflow webserver --port 8080

airflow schedule


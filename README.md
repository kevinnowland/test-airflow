# Testing Airflow

Repo to contains code related to testing out Apache Airflow.

There is a python package called `dummy_etl` in that folder
which can be installed via
```bash
git clone https://github.com/kevinnowland/test-airflow
cd test-airflow/dummy_etl
pip install git+https://github.com/kevinnowland/test-airflow/tree/main/dummy_etl
cd ../..
rm -rf test-airflow
```

This package is used in the workflow defined in the `reddit_etl.py` module.

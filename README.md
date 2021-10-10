# Testing Airflow

Repo to contains code related to testing out Apache Airflow.

I setup a demo ETL job that extracts some top comments
from a couple subreddits, transforms some of the words
into word vector features, then uploads these words to
a DynamoDB no-sql database table that I provisioned in
the [AWS Terraform](https://github.com/kevinnowland/aws-terraform)
repo.

There is a python package called `dummy_etl` in that folder
which can be installed via
```bash
git clone https://github.com/kevinnowland/test-airflow
cd test-airflow/dummy_etl
pip install .
cd ../..
rm -rf test-airflow
```

This package is used in the workflow defined in the `reddit_etl.py` module.

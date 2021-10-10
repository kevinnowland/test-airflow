""" module to load the reddit secrets """


import boto3
import json


def get_reddit_secrets() -> dict:
    """ get the reddit secrets.

    Assumes you have access to these secrets already,
    probably by being me and having run `aws configure`
    """

    secret_client = boto3.client('secretsmanager')
    secret = secret_client.get_secret_value(SecretId='knowland-reddit-secrets')
    secret_json = json.loads(secret['SecretString'])
    return dict(secret_json)

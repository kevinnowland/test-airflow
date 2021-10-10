"""" module to load into dynamodb table  """

import boto3
from botocore.exceptions import ParamValidationError
import os
import re
from typing import List, Dict
import yaml


def get_processed_filenames(dir_path: str) -> List[str]:
    """ find appropriate filenames """

    all_files = os.listdir(dir_path)
    file_pattern = re.compile(r'\d{12}_PROCESSED.yml')
    matching_files = [f for f in all_files if file_pattern.search(f)]

    return [
        dir_path + '/' + f
        for f in matching_files
    ]


def load_comment(dynamo_client,
                 table_name: str,
                 comment: Dict,
                 subreddit: str) -> bool:
    """ load single comment into table """
    table_name = 'reddit_comments'

    single_fields = {
        'subreddit': {'S': subreddit},
        'username': {'S': comment['username']},
        'comment_id': {'S': comment['comment_id']}
    }

    word_vecs = [ 
        word_vec.split(',')
        for word_vec in comment['word_vecs'].strip().split('\n')
    ]

    word_vector_dict = {
        'word' + str(i): {'NS': word_vecs[i]}
        for i in range(len(word_vecs))
    }

    item_dict = dict(single_fields, **word_vector_dict)

    try:
        dynamo_client.put_item(TableName=table_name, Item=item_dict)
        return True
    except ParamValidationError:
        raise


def load_filename(filename: str, dynamo_client, table_name: str) -> bool:
    """ load all comments from a single file """

    raw_name = filename.split('/')[-1]
    subreddit = raw_name.split('_')[0]

    with open(filename, 'r') as f:
        comment_yaml = yaml.safe_load(f)

    comment_statuses = [
        load_comment(dynamo_client, table_name, comment, subreddit)
        for comment in comment_yaml['comments']
    ]

    return all(comment_statuses)


def load_directory(dir_path: str) -> bool:
    """ load files into the dynamo db """

    processed_files = get_processed_filenames(dir_path)
    table_name = 'reddit_comments'
    dynamo_client = boto3.client('dynamodb')

    file_statuses = [
        load_filename(filename, dynamo_client, table_name)
        for filename in processed_files
    ]

    return all(file_statuses)

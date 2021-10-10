""" module to load the reddit secrets """


import boto3
from datetime import datetime
import json
from praw import Reddit
from praw.models.reddit.comment import Comment
from typing import List


def get_reddit_secrets() -> dict:
    """ get the reddit secrets.

    Assumes you have access to these secrets already,
    probably by being me and having run `aws configure`
    """

    secret_client = boto3.client('secretsmanager')
    secret = secret_client.get_secret_value(SecretId='knowland-reddit-secrets')
    secret_json = json.loads(secret['SecretString'])
    return dict(secret_json)


def load_reddit() -> Reddit:
    """ load subreddit """
    secrets = get_reddit_secrets()
    reddit = Reddit(username=secrets['username'],
                    user_agent=secrets['user_agent'],
                    client_id=secrets['client_id'],
                    client_secret=secrets['secret'])
    return reddit


def extract_raw_comments(subreddit_name: str) -> List[Comment]:
    """ find top submissions in past week and choose a couple
    comments from them. """

    reddit = load_reddit()
    subreddit = reddit.subreddit(subreddit_name)
    top_submissions = subreddit.top('week', limit=5)

    def get_top_comments(submission):
        """ get a few comments per submission as long
        as they are at least 200 characters long """
        submission.comments.replace_more(limit=0)
        comments = [c for c in submission.comments if len(c.body) > 100]
        comments.sort(key=lambda c: c.score, reverse=True)
        return comments[:2]

    top_comments = [
        comment
        for submission in top_submissions
        for comment in get_top_comments(submission)
    ]

    return top_comments


def save_raw_comments(subreddit_name: str, comments: List[Comment], dir_path: str) -> None:
    """ save comment username, id, and body in csv NO HEADER """

    now_str = datetime.now().strftime('%Y%m%d%H%M')
    file_name = dir_path + '/' + subreddit_name + '_' + now_str + '.csv'

    with open(file_name, 'w') as f:
        for comment in comments:
            comment_str = comment.author.name
            comment_str += ',' + comment.id
            comment_str += ',' + comment.body.replace('\n', '').replace(',', '') + '\n'
            f.write(comment_str)


def extract_subreddit_comments(subreddit_name: str, dir_path: str) -> None:
    """ save some top comments from the given subredit
    to disk with format subredditname_timestamp.csv
    """

    comments = extract_raw_comments(subreddit_name)
    save_raw_comments(subreddit_name, comments, dir_path)

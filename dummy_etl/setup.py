from setuptools import setup

# make the README into the long description
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="dummy_etl",
    version="0.1",
    description="reddit comment etl"
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/kevinnowland/dummy_etl",
    author="Kevin Nowland",
    license="MIT",
    packages=["dummy_etl"],
    install_requires=[
        'spacy==3.1.3',
        'en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.1.0/en_core_web_sm-3.1.0.tar.gz',
        'boto3>=1.18',
        'praw>=7.4'
    ],
    zip_safe=False
)

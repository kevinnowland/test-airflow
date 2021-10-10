""" module to transform reddit comments and save them locally """

import itertools
import numpy
import os
import re
import spacy
from typing import List


class CommentToVecError(Exception):
    pass


def get_raw_filenames(dir_path: str) -> List[str]:
    """ find appropriate filenames """

    all_files = os.listdir(dir_path)
    file_pattern = re.compile(r'\d{12}.csv')
    matching_files = [f for f in all_files if file_pattern.search(f)]

    return [
        dir_path + '/' + f
        for f in matching_files
    ]


def comment_to_vecs(comment: str) -> List[List[numpy.float32]]:
    """ process comment into a list of vectors.
    Limiting to only 20 words per comment in response
    """

    nlp = spacy.load('en_core_web_sm')

    # define objects needed for cleaning
    regexes = {
        'weird_chars': re.compile(r'[\?;\(\)\\.,\!:–\-\"\[\]“”]'),
        'newlines': re.compile(r'\n'),
        'html': re.compile(r'<[^<]+/>', re.MULTILINE),
        'urls': re.compile(r'^https?://.*[rn]*', re.MULTILINE),
        'spaces': re.compile(r'\s{2,}'),
        'u': re.compile(r'\bu\b')
    }

    allowed_stops = ['no', 'never', 'not', 'none', 'up', 'down',
                     'back', 'over', 'under', 'two', 'three']
    stop_words = [
        word for word in nlp.Defaults.stop_words
        if word not in allowed_stops
    ]
    stop_words += ['-PRON-']

    # clean the comment
    comment = comment.lower()

    # custom replacements we decided on
    comment = comment.replace('`', '\'')
    comment = comment.replace('’', '\'')

    comment = comment.replace("won't", "will not")
    comment = comment.replace("n't", " not")

    comment = regexes['u'].sub('you', comment)
    comment = regexes['html'].sub(' ', comment)
    comment = regexes['urls'].sub(' ', comment)
    comment = regexes['weird_chars'].sub(' ', comment)
    comment = regexes['newlines'].sub(' ', comment)
    comment = regexes['spaces'].sub(' ', comment)

    # removing the multiletters such as 'happppy' -> 'happy'
    comment = ''.join(''.join(s)[:2] for _, s in itertools.groupby(comment))

    # lemmatize
    comment = ' '.join([word.lemma_ for word in nlp(comment)])

    # remove stopwords
    comment = ' '.join([w for w in comment.split(' ') if w not in stop_words])

    word_vecs = [list(word.vector) for word in nlp(comment)]

    return word_vecs[:20]


def transform_file(filename: str) -> bool:
    """ read in comment file and write to processed version of file
    assumes filename ends in .csv

    Assumes format is username, comment_id, body
    with no header

    output is YAML with format

    comments:
        - comment_id: som374
          username: name
          word_vecs: |
            [2,45,234,3]
            [10,13,37,23]
    """

    processed_filename = filename[:-4] + '_PROCESSED.yml'

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return False

    try:
        with open(processed_filename, 'w') as f:
            f.write('comments:\n')

            for line in lines:
                splits = line.split(',')
                f.write('    - comment_id: ' + splits[1] + '\n')
                f.write('      username: ' + splits[0] + '\n')
                f.write('      word_vecs: |\n')

                word_vecs = comment_to_vecs(splits[2])

                for vec in word_vecs:
                    f.write('        ' + str(vec)[1:-1].replace(' ', '') + '\n')
    except CommentToVecError:
        return False

    return True


def transform_directory(dir_path: str) -> bool:
    """ process all raw files in a directory """
    raw_files = get_raw_filenames(dir_path)
    return all([transform_file(filename) for filename in raw_files])

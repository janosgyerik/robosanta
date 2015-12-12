import logging

import os
import random
import requests
import settings
from bs4 import BeautifulSoup
from robosanta.stackexchange.sede import extract_column
from stackexchange import CodeReview

''' TODO : better separation of concerns
caching sede downloader
  try to download
  if not empty: update cache, return content
  else
    log a warning
    return from cache

message provider
  message = optional intro + link

sede message provider
  pick a line, extracting columns from sede + shuffle + filtering

naruto message provider
  compose from sede message provider
  custom intro message
  sede configuration
    sede url
    column to pick
  filter logic:
    fetch answer
    reject if author is in exclusion list
    reject if answer author is same as question author
    reject if question is closed
    reject if answer score is not 0
    accept

forgotten zombie message provider
  compose from sede message provider
  custom intro message
  sede configuration
    sede url
    column to pick
  filter logic:
    fetch question
    reject if closed
    reject if accepted
    reject if any answer has score > 0
    reject if no answer has score == 0
    accept
'''


NARUTO_URL = 'http://data.stackexchange.com/codereview/query/264586/naruto-accepted-answer-with-zero-score'
NARUTO_INTRO_MESSAGE = 'Accepted non-selfie answer with 0 score:'
NARUTO_CACHE = '.cache/naruto.html'


def pick_naruto_message():
    logging.info('fetching Naruto posts')
    html = requests.get(NARUTO_URL).text
    soup = BeautifulSoup(html)

    def extract_answer_ids():
        data = extract_column(soup, 'Post Link')
        return [value['id'] for value in data]

    answer_ids = extract_answer_ids()

    if answer_ids:
        logging.info('updating Naruto cache')
        with open(NARUTO_CACHE, 'w') as fh:
            fh.write(html)
    else:
        logging.warning('no Naruto posts...')
        if os.path.exists(NARUTO_CACHE):
            logging.info('using previous cache of Naruto posts')
            with open(NARUTO_CACHE) as fh:
                soup = BeautifulSoup(fh)
            answer_ids = extract_answer_ids()
        else:
            answer_ids = []

    random.shuffle(answer_ids)

    cr = CodeReview()
    for answer_id in answer_ids:
        try:
            logging.info('fetching answer {}'.format(answer_id))
            answer = cr.answer(answer_id)
        except ValueError:
            continue

        if answer.owner_id in settings.EXCLUDED_OWNERS:
            logging.warning('owner excluded, skip: {}'.format(answer.url))
            continue

        question = cr.question(answer.question_id)
        if 'closed_date' in question.json:
            logging.warning('question closed, skip: {}'.format(answer.url))
            continue

        if answer and answer.score == 0:
            return [NARUTO_INTRO_MESSAGE, answer.url]

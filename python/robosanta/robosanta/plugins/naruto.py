import logging
import random

import settings
from robosanta.stackexchange import sede
from stackexchange import CodeReview

''' TODO : better separation of concerns
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
    +reject if author is in exclusion list
    reject if answer author is same as question author
    reject if question is closed
    +reject if answer score is not 0
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


def pick_naruto_message():
    cols, rows = sede.fetch_table('naruto', NARUTO_URL)

    answer_id_index = cols['Post Link']['index']
    answer_ids = [row[answer_id_index]['id'] for row in rows]

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

import logging

import settings
from robosanta.plugins.pickers import PostPicker
from stackexchange import CodeReview

''' TODO
  filter logic:
    fetch answer
    +reject if author is in exclusion list
    reject if answer author is same as question author
    reject if question is closed
    +reject if answer score is not 0
    accept
'''

URL = 'http://data.stackexchange.com/codereview/query/264586/naruto-accepted-answer-with-zero-score'
INTRO_MESSAGE = 'Accepted non-selfie answer with 0 score:'


class NarutoPicker(PostPicker):

    def __init__(self):
        super().__init__()
        self.cr = CodeReview()

    @property
    def name(self):
        return 'naruto'

    @property
    def url(self):
        return URL

    def accept(self, post_id):
        logging.info('fetching answer {}'.format(post_id))
        try:
            answer = self.cr.answer(post_id)
        except ValueError as e:
            logging.error('error when fetching answer: '.format(e))
            return None

        if answer.owner_id in settings.EXCLUDED_OWNERS:
            logging.info('owner excluded, skip: {}'.format(answer.url))
            return None

        question = self.cr.question(answer.question_id)
        if 'closed_date' in question.json:
            logging.warning('question closed, skip: {}'.format(answer.url))
            return None

        if answer.score != 0:
            logging.warning('score not zero, skip: {}'.format(answer.url))
            return None

        return [INTRO_MESSAGE, answer.url]

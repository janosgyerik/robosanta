import logging

import settings
from robosanta.plugins.pickers import PostPicker
from stackexchange import CodeReview

URL = 'http://data.stackexchange.com/codereview/query/264586/naruto-accepted-answer-with-zero-score'
INTRO_MESSAGE = 'Naruto answer; accepted non-selfie answer with 0 score:'


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
        """
        memo: deleted answers are excluded by Stack API
        memo: deleted questions are excluded by Stack API

        :param post_id: is of a question
        :return: messages to send, or falsy to reject
        """
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

        if question.owner_id == answer.owner_id:
            logging.warning('answer owner is the same as question owner, skip: {}'.format(answer.url))
            return None

        if answer.score != 0:
            logging.warning('score not zero, skip: {}'.format(answer.url))
            return None

        return [INTRO_MESSAGE, answer.url]

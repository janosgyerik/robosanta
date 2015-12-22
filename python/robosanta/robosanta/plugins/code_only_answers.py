import logging

from robosanta.plugins.pickers import PostPicker
from stackexchange import CodeReview

URL = 'http://data.stackexchange.com/codereview/query/324265/code-only-answers'
INTRO_MESSAGE = 'Code-only answer:'


class CodeOnlyAnswerPicker(PostPicker):

    def __init__(self):
        super().__init__()
        self.cr = CodeReview()

    @property
    def name(self):
        return 'code-only-answer'

    @property
    def url(self):
        return URL

    def accept(self, post_id):
        """
        memo: deleted answers are excluded by Stack API
        memo: deleted questions are excluded by Stack API

        :param post_id: id of an answer
        :return: messages to send, or falsy to reject
        """
        logging.info('fetching answer {}'.format(post_id))
        try:
            answer = self.cr.answer(post_id)
        except ValueError as e:
            logging.error('error when fetching answer: '.format(e))
            return None

        if answer.is_accepted:
            logging.info('answer is accepted, skip: {}'.format(answer.id))
            return None

        if answer.score != 0:
            logging.info('answer has score != 0, skip: {}'.format(answer.id))
            return None

        logging.info('fetching question {}'.format(answer.question_id))
        try:
            question = self.cr.question(answer.question_id)
        except ValueError as e:
            logging.error('error when fetching answer: '.format(e))
            return None

        if 'closed_date' in question.json:
            logging.warning('question closed, skip: {}'.format(answer.url))
            return None

        return [INTRO_MESSAGE, answer.url]

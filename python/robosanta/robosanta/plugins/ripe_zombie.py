import logging

from robosanta.plugins.pickers import PostPicker
from stackexchange import CodeReview

RIPE_ZOMBIE_URL = 'http://data.stackexchange.com/codereview/query/412155/ripe-zombies'
INTRO_MESSAGE = 'TODO:'


class RipeZombiePicker(PostPicker):

    def __init__(self):
        super().__init__()
        self.cr = CodeReview()

    @property
    def name(self):
        return 'ripe-zombie'

    @property
    def url(self):
        return RIPE_ZOMBIE_URL

    def accept(self, post_id):
        """
        memo: deleted answers are excluded by Stack API
        memo: deleted questions are excluded by Stack API

        :param post_id: post id in the query
        :return: tuple of (post url, accept/reject)
        """

        reject = (None, False)

        logging.info('fetching question {}'.format(post_id))
        try:
            question = self.cr.question(post_id)
        except ValueError as e:
            logging.error('error when fetching question: '.format(e))
            return reject

        if 'closed_date' in question.json:
            logging.warning('question closed, skip: {}'.format(question.url))
            return reject

        score_0_exists = False

        for answer in question.answers:
            if answer.score > 0:
                logging.warning('answer with postitive score exists, skip: {}'.format(answer.url))
                return reject

            if answer.is_accepted:
                logging.warning('accepted answer exists, skip: {}'.format(answer.url))
                return reject

            if answer.score == 0:
                score_0_exists = True

        if not score_0_exists:
            logging.warning('no answer with 0 score, skip: {}'.format(question.url))
            return reject

        return [INTRO_MESSAGE, question.url], True

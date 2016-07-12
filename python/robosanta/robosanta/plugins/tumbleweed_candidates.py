import logging

from robosanta.plugins.pickers import PostPicker, format_post
from stackexchange import CodeReview

URL = 'http://data.stackexchange.com/codereview/query/508754/tumbleweed-prevention'
DESCRIPTION_URL = 'http://meta.codereview.stackexchange.com/a/4947/12390'
DESCRIPTION = '[Tumbleweed candidate]({}); zero score, no answers, no comments, and low views'.format(DESCRIPTION_URL)


class TumbleweedCandidatePicker(PostPicker):

    def __init__(self):
        super().__init__()
        self.cr = CodeReview()

    @property
    def url(self):
        return URL

    def accept(self, post_id):
        """
        memo: deleted questions are excluded by Stack API

        :param post_id: id of a question
        :return: messages to send, or falsy to reject
        """
        logging.info('fetching question {}'.format(post_id))
        try:
            question = self.cr.question(post_id)
        except ValueError as e:
            logging.error('error when fetching question: '.format(e))
            return None

        if 'closed_date' in question.json:
            logging.warning('question closed, skip: {}'.format(question.url))
            return None

        if question.score != 0:
            logging.warning('question has non-zero score, skip: {}'.format(question.url))
            return None

        if question.answers:
            logging.warning('question has answers, skip: {}'.format(question.url))
            return None

        if question.comments.fetch():
            logging.warning('question has comments, skip: {}'.format(question.url))
            return None

        return format_post(DESCRIPTION, question.title, question.url, question.tags)

import logging

from robosanta.plugins.pickers import PostPicker, format_post
from stackexchange import CodeReview

URL = 'http://data.stackexchange.com/codereview/query/264586/naruto'
DESCRIPTION_URL = 'http://meta.codereview.stackexchange.com/a/4946/12390'
DESCRIPTION = '[Naruto answer]({}); accepted non-selfie answer with 0 score'.format(DESCRIPTION_URL)


class NarutoPicker(PostPicker):

    def __init__(self):
        super().__init__()
        self.cr = CodeReview()

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

        if not answer.is_accepted:
            logging.warning('answer not accepted, skip: {}'.format(answer.url))
            return None

        if answer.score != 0:
            logging.warning('score not zero, skip: {}'.format(answer.url))
            return None

        question = self.cr.question(answer.question_id)

        if 'closed_date' in question.json:
            logging.warning('question closed, skip: {}'.format(answer.url))
            return None

        if question.owner_id == answer.owner_id:
            logging.warning('answer owner is the same as question owner, skip: {}'.format(answer.url))
            return None

        return format_post(DESCRIPTION, question.title, answer.url, question.tags)

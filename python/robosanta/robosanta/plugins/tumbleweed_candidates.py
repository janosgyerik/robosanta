import json
import logging
import requests

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

        if self.recently_awarded_tumbleweed(question.owner_id, question.creation_date):
            logging.warning('owner has recently received tumbleweed, skip: {}'.format(question.url))
            return None

        return format_post(DESCRIPTION, question.title, question.url, question.tags)

    def recently_awarded_tumbleweed(self, user_id, date):
        badge_id = self.cr.badge(name='Tumbleweed').id
        fromdate = int(date.timestamp())
        url = 'https://api.stackexchange.com/2.2/badges/{}/recipients'.format(badge_id)
        data = {
            'fromdate': fromdate,
            'site': 'codereview',
        }
        response = requests.get(url, data)
        if not response.ok:
            return self.has_tumbleweed(user_id)

        items = json.loads(response.content.decode())['items']
        return user_id in [item['user']['user_id'] for item in items]

    def has_tumbleweed(self, owner_id):
        user = self.cr.user(owner_id)
        return any([badge.name == 'Tumbleweed' for badge in user.badges.fetch()])

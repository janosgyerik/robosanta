import logging

from robosanta.stackexchange.chat import browser


class Client(object):
    def __init__(self):
        self._browser = browser.Browser()

    def login(self, email, password):
        logging.info("Logging in.")

        self._browser.login_se_openid(email, password)
        self._browser.login_site()
        self._browser.login_chat()

        logging.info("Login OK")

    def post_message(self, room_id, text):
        logging.info('sending message to room {}: {}'.format(room_id, text))
        self._browser.send_message(room_id, text)

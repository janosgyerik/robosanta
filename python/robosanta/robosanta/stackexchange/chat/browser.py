# encoding: utf-8

from bs4 import BeautifulSoup
import requests


USER_AGENT = 'StackExchangeChatCLI/0.dev'
REQUEST_TIMEOUT = 30

SE_OPENID = 'https://openid.stackexchange.com'
SE_OPENID_LOGIN_ROOT = SE_OPENID + '/account/login'
SE_LOGIN_ROOT = 'http://stackexchange.com/users'

CHAT_ROOT = 'http://chat.stackexchange.com'


class Browser(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT
        })
        self.chat_fkey = None

    # request helpers

    def _request(self, method, url, data=None, headers=None):
        method_method = getattr(self.session, method)
        return method_method(url, data=data, headers=headers, timeout=REQUEST_TIMEOUT)

    def get(self, url, data=None, headers=None):
        return self._request('get', url, data, headers)

    def post(self, url, data=None, headers=None):
        return self._request('post', url, data, headers)

    def get_soup(self, url, data=None, headers=None):
        response = self.get(url, data, headers)
        return BeautifulSoup(response.content, "html.parser")

    def get_fkey(self, url):
        fkey_soup = self.get_soup(url)
        fkey_input = fkey_soup.find('input', {'name': 'fkey'})
        return fkey_input['value']

    # authentication

    def login_se_openid(self, user, password):
        self.post(
            SE_OPENID_LOGIN_ROOT + '/submit',
            {
                'email': user,
                'password': password,
                'fkey': self.get_fkey(SE_OPENID_LOGIN_ROOT),
            }
        )

    def login_site(self):
        self.post(
            SE_LOGIN_ROOT + '/authenticate',
            {
                'openid_identifier': SE_OPENID,
                'fkey': self.get_fkey(SE_LOGIN_ROOT + '/login'),
            }
        )

    def login_chat(self):
        self.chat_fkey = self.get_fkey(CHAT_ROOT + '/chats/join/favorite')

    # remote requests

    def send_message(self, room_id, text):
        return self.post(
            CHAT_ROOT + '/chats/{}/messages/new'.format(room_id),
            {
                'text': text,
                'fkey': self.chat_fkey
            })

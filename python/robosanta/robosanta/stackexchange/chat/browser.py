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

    def _se_openid_login_with_fkey(self, fkey_url, post_url, data):
        data['fkey'] = self.get_fkey(fkey_url)
        self.post(post_url, data)

    def login_se_openid(self, user, password):
        self._se_openid_login_with_fkey(
            SE_OPENID_LOGIN_ROOT,
            SE_OPENID_LOGIN_ROOT + '/submit',
            {
                'email': user,
                'password': password,
            })

    def login_site(self):
        self._se_openid_login_with_fkey(
            SE_LOGIN_ROOT + '/login',
            SE_LOGIN_ROOT + '/authenticate',
            {
                'openid_identifier': SE_OPENID
            })

    def login_chat(self):
        fkey_url = CHAT_ROOT + '/chats/join/favorite'
        self.chat_fkey = self.get_fkey(fkey_url)

    # remote requests

    def send_message(self, room_id, text):
        return self.post(
            CHAT_ROOT + '/chats/{}/messages/new'.format(room_id),
            {
                'text': text,
                'fkey': self.chat_fkey
            })

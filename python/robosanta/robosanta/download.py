import logging

import os
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.join(BASE_DIR, '.cache')


def fetch_soup(label, url):
    def is_valid(soup):
        for script in soup.findAll('script'):
            result_sets_col = 'resultSets'
            if result_sets_col in script.text:
                return True
        return False

    if not os.path.isdir(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    logging.info('fetching {} as {}'.format(label, url))
    html = requests.get(url).text
    soup = BeautifulSoup(html)

    cache_path = os.path.join(CACHE_DIR, '{}.html'.format(label))
    debug_cache_path = os.path.join(CACHE_DIR, '{}-debug.html'.format(label))

    if is_valid(soup):
        logging.info('updating cache')
        with open(cache_path, 'w') as fh:
            fh.write(html)
        return soup

    with open(debug_cache_path, 'w') as fh:
        fh.write(html)

    logging.warning('result not valid')
    if os.path.exists(cache_path):
        logging.info('using previous cache')
        with open(cache_path) as fh:
            return BeautifulSoup(fh)

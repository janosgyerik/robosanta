import json
import logging
import os

import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.join(BASE_DIR, '.cache')


def extract_column(soup, colname):
    """
    Returns a generator of cell values in selected column.

    For simple columns like timestamp, a cell value can be simple,
    for example: 1414433013197

    For more complex columns like Post Link, a cell value can be an object,
    for example:

      {
        "id": 68102,
        "title": "Bash Script - File Comment out & Notate"
      }

    :param soup: a bs4 (BeautifulSoup) object
    :param colname: name of the SEDE column to extract
    :return: generator of cell values in selected column
    """

    def get_column_index():
        for index, info in enumerate(columns):
            if info['name'] == colname:
                return index
        return -1

    for script in soup.findAll('script'):
        result_sets_col = 'resultSets'
        if result_sets_col in script.text:
            start = script.text.rindex('{', 0, script.text.index(result_sets_col))
            end = script.text.index('}', script.text.index('querySetId')) + 1
            data = json.loads(script.text[start:end])

            results = data[result_sets_col][0]
            columns = results['columns']
            rows = results['rows']

            column_index = get_column_index()
            if column_index > -1:
                for row in rows:
                    yield row[column_index]


def transform_columns_meta(se_columns_meta):
    columns_meta = {}

    for index, se_col_meta in enumerate(se_columns_meta):
        col_meta = {'index': index}
        col_meta.update(se_col_meta)
        columns_meta[se_col_meta['name']] = col_meta

    return columns_meta


def extract_table(soup):
    for script in soup.findAll('script'):
        result_sets_col = 'resultSets'
        if result_sets_col in script.text:
            start = script.text.rindex('{', 0, script.text.index(result_sets_col))
            end = script.text.index('}', script.text.index('querySetId')) + 1
            data = json.loads(script.text[start:end])

            results = data[result_sets_col][0]
            columns = transform_columns_meta(results['columns'])
            rows = results['rows']

            return columns, rows

    return {}, []


def fetch_table(label, url):
    """
    Fetch a URL using `fetch_soup` and extract a table as a tuple of {cols} and [rows].
    {cols} is a mapping of column names to column meta data, see more details below.
    [rows] is a list of rows in the table.

    Example values of {cols}:
        {
            'name': {
                'index': 0,
                'type': 'User',
            }
        }

    :param label: a simple name to represent the URL, it will be used as the cache filename
    :param url: the URL to download
    :return: a tuple of ({cols}, [rows])
    """
    soup = fetch_sede_soup(label, url)
    if not soup:
        return {}, []

    return extract_table(soup)


def fetch_sede_soup(label, url):
    cache_path = os.path.join(CACHE_DIR, '{}.html'.format(label))
    debug_cache_path = os.path.join(CACHE_DIR, '{}-debug.html'.format(label))

    if not os.path.isdir(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    logging.info('fetching {} as {}'.format(label, url))
    html = requests.get(url).text
    soup = BeautifulSoup(html)

    def is_valid(soup):
        for script in soup.findAll('script'):
            if 'resultSets' in script.text:
                return True
        return False

    def write_cache(path, html):
        with open(path, 'w') as fh:
            fh.write(html)

    if is_valid(soup):
        logging.info('updating cache')
        write_cache(cache_path, html)
        return soup

    write_cache(debug_cache_path, html)

    logging.warning('result not valid')
    if os.path.exists(cache_path):
        logging.info('using previous cache')
        with open(cache_path) as fh:
            return BeautifulSoup(fh)

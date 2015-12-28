import json
import logging
import os

import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.join(BASE_DIR, '.cache')


class Table:
    """
    Represent the results of a SEDE query.

    For simple columns like timestamp, a cell value can be simple,
    for example: 1414433013197

    For more complex columns like Post Link, a cell value can be an object,
    for example:

      {
        "id": 68102,
        "title": "Bash Script - File Comment out & Notate"
      }
    """

    def __init__(self, columns=None, rows=None):
        """
        Create a Table from columns meta data and rows.

        :param columns: meta data of columns as a dict
        :param rows: rows of the table as list of dict
        :return: new Table instance
        """
        if not columns:
            columns = {}
        if not rows:
            rows = []
        self._columns = columns
        self._rows = rows
        self._colnames = set(columns.keys())

    @property
    def colnames(self):
        """
        Get list of column names

        :return: list of column names
        """
        return self._colnames

    def column(self, name):
        """
        Get column, by iterating over rows and extracting specified column.

        :param name: name of the column to extract
        :return: content of the column as a list
        """
        index = self._columns[name]['index']
        return [row[index] for row in self._rows]

    def post_ids(self):
        """
        Convenience method to extract the ids from a Post Link column.

        :return: list of post ids
        """
        return [post_link['id'] for post_link in self.column('Post Link')]


def fetch_sede_soup(label, url):
    """
    Download the result page of a SEDE query and create a BeautifulSoup from it.
    If the page contains results, cache it in a file.
    If the page doesn't contain results, use the cache instead.
    Note: this happens when the SEDE query is not executed in the browser
    for a few days.

    :param label: a simple name to represent the URL, it will be used as the cache filename
    :param url: the URL to download
    :return: a BeautifulSoup instance from the URL
    """

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
    else:
        logging.warning('result not valid')
        write_cache(debug_cache_path, html)

    if os.path.exists(cache_path):
        logging.info('using previous cache')
        with open(cache_path) as fh:
            return BeautifulSoup(fh)
    else:
        logging.error('no previous cache: you must download the page manually')
        return BeautifulSoup()


def fetch_table(label, url):
    """
    Fetch a URL using `fetch_soup` and extract to a Table.

    :param label: a simple name to represent the URL, it will be used as the cache filename
    :param url: the URL to download
    :return: the Table representing the SEDE results, or None if fetch failed
    """
    soup = fetch_sede_soup(label, url)
    if not soup:
        return None

    return extract_table(soup)


def transform_columns_meta(se_columns_meta):
    """
    Transform SE column meta data, for example,
    from:
        [
            {'name': 'User Link', 'type': 'User'},
            {'name': 'Post Link', 'type': 'Post'}
        ]
    to:
        {
            'User Link': {'name': 'User Link', 'type': 'User', 'index': 0},
            'Post Link': {'name': 'Post Link', 'type': 'Post', 'index': 1}
        }

    :param se_columns_meta: list of dictionaries describing the fields
    :return: dictionary of dictionaries, with index added
    """
    columns_meta = {}

    for index, se_col_meta in enumerate(se_columns_meta):
        col_meta = {'index': index}
        col_meta.update(se_col_meta)
        columns_meta[se_col_meta['name']] = col_meta

    return columns_meta


def extract_table(soup):
    """
    Return a Table representing the SEDE results

    :param soup: a bs4 (BeautifulSoup) object
    :return: a Table object
    """
    for script in soup.findAll('script'):
        result_sets_col = 'resultSets'
        if result_sets_col in script.text:
            start = script.text.rindex('{', 0, script.text.index(result_sets_col))
            end = script.text.index('}', script.text.index('querySetId')) + 1
            data = json.loads(script.text[start:end])

            results = data[result_sets_col][0]
            columns = transform_columns_meta(results['columns'])
            rows = results['rows']

            return Table(columns, rows)

    return Table()

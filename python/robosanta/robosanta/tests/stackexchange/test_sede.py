import os
import unittest

from bs4 import BeautifulSoup
from robosanta.stackexchange.sede import extract_column

BASE_DIR = os.path.dirname(__file__)

SEDE_OUTPUT_HTML = os.path.join(BASE_DIR, 'sede-output.html')
POST_ID_COLUMN = 'Post Link'
DATE_COLUMN = 'CreationDate'
ROW_COUNT = 49


def new_soup():
    with open(SEDE_OUTPUT_HTML) as fh:
        return BeautifulSoup(fh)


class TestGetColumn(unittest.TestCase):
    def extract_column(self, colname):
        return extract_column(new_soup(), colname)

    def extract_post_link(self):
        return self.extract_column(POST_ID_COLUMN)

    def extract_date(self):
        return self.extract_column(DATE_COLUMN)

    def test_row_count_of_post_link(self):
        self.assertEqual(ROW_COUNT, len(list(self.extract_post_link())))

    def test_first_post_link(self):
        expected = {
            'title': 'TinyMVC Model / Plugin how to implement?',
            'id': 12144,
        }
        self.assertEqual(expected, next(self.extract_post_link()))

    def test_row_count_of_date(self):
        self.assertEqual(ROW_COUNT, len(list(self.extract_date())))

    def test_first_date(self):
        self.assertEqual(1338304381360, next(self.extract_date()))

    def test_nonexistent_column(self):
        with self.assertRaises(StopIteration):
            next(self.extract_column('nonexistent'))


if __name__ == '__main__':
    unittest.main()

import os
import unittest

from bs4 import BeautifulSoup
from robosanta.stackexchange.sede import _extract_table

BASE_DIR = os.path.dirname(__file__)

SEDE_OUTPUT_HTML = os.path.join(BASE_DIR, 'sede-output.html')
POST_ID_COLUMN = 'Post Link'
DATE_COLUMN = 'CreationDate'
ROW_COUNT = 49


def new_soup():
    with open(SEDE_OUTPUT_HTML) as fh:
        return BeautifulSoup(fh)


def new_table():
    return _extract_table(new_soup())


class TestGetColumn(unittest.TestCase):
    def extract_column(self, colname):
        return _extract_table(new_soup()).column(colname)

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
        self.assertEqual(expected, self.extract_post_link()[0])

    def test_row_count_of_date(self):
        self.assertEqual(ROW_COUNT, len(self.extract_date()))

    def test_first_date(self):
        self.assertEqual(1338304381360, self.extract_date()[0])

    def test_nonexistent_column(self):
        with self.assertRaises(KeyError):
            self.extract_column('nonexistent')


class TestTable(unittest.TestCase):

    def test_colnames(self):
        self.assertEqual({'User Link', 'Post Link', 'CreationDate'}, new_table().colnames)

    def test_post_ids(self):
        self.assertEqual([12144, 13224, 13542, 20870, 25280], new_table().post_ids()[:5])

    def test_column_CreationDate(self):
        self.assertEqual([1338304381360, 1341070257150], new_table().column('CreationDate')[:2])

    def test_post_link_title(self):
        self.assertEqual([
            'TinyMVC Model / Plugin how to implement?',
            'Encapsulation of client side logic in web page'
        ], [link['title'] for link in new_table().column('Post Link')][:2])

if __name__ == '__main__':
    unittest.main()

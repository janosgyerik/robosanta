#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

from robosanta.stackexchange import sede

URLS = {
    'code-only-answers': 'http://data.stackexchange.com/codereview/query/324265/code-only-answers',
    'bad-naruto': 'http://data.stackexchange.com/codereview/query/267209/bad-naruto',
    'naruto': 'http://data.stackexchange.com/codereview/query/264586/naruto-accepted-answer-with-zero-score',
    'forgotten-zombie-killers': 'http://data.stackexchange.com/codereview/query/265223/forgotten-zombie-killers',
}


def parse_args():
    parser = ArgumentParser(description='Scrape data from SEDE queries')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('--naruto', action='store_true')
    parser.add_argument('--bad-naruto', action='store_true')
    parser.add_argument('--code-only-answers', action='store_true')
    parser.add_argument('--forgotten-zombie-killers', action='store_true')
    parser.add_argument('-u', '--url')

    args = parser.parse_args()

    if args.quiet:
        logging.basicConfig(level=logging.WARN)
    else:
        logging.basicConfig(level=logging.INFO)

    for label in URLS:
        if getattr(args, label.replace('-', '_'), False):
            break
    else:
        return

    url = URLS[label]

    cols, rows = sede.fetch_table(label, url)
    sorted_cols = sorted(cols.items(), key=lambda x: x[1]['index'])

    for row in rows:
        for col_item in sorted_cols:
            col = col_item[1]
            print('{}: {}'.format(col['name'], row[col['index']]))
        print()


def main():
    parse_args()


if __name__ == '__main__':
    main()

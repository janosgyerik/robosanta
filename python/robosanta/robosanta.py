#!/usr/bin/env python3

import logging
import os
import random
from argparse import ArgumentParser

import requests
import settings
from bs4 import BeautifulSoup
from robosanta.stackexchange.chat.client import Client
from robosanta.stackexchange.sede import extract_column
from stackexchange import CodeReview

NARUTO_URL = 'http://data.stackexchange.com/codereview/query/264586/naruto-accepted-answer-with-zero-score'
NARUTO_INTRO_MESSAGE = 'Accepted non-selfie answer with 0 score:'
NARUTO_CACHE = '.cache/naruto.html'


def naruto():
    logging.info('fetching Naruto posts')
    html = requests.get(NARUTO_URL).text
    soup = BeautifulSoup(html)

    def extract_answer_ids():
        data = extract_column(soup, 'Post Link')
        return [value['id'] for value in data]

    answer_ids = extract_answer_ids()

    if answer_ids:
        logging.info('updating Naruto cache')
        with open(NARUTO_CACHE, 'w') as fh:
            fh.write(html)
    else:
        logging.warning('no Naruto posts...')
        if os.path.exists(NARUTO_CACHE):
            logging.info('using previous cache of Naruto posts')
            with open(NARUTO_CACHE) as fh:
                soup = BeautifulSoup(fh)
            answer_ids = extract_answer_ids()
        else:
            answer_ids = []

    random.shuffle(answer_ids)

    cr = CodeReview()
    for answer_id in answer_ids:
        try:
            logging.info('fetching answer {}'.format(answer_id))
            answer = cr.answer(answer_id)
        except ValueError:
            continue

        if answer.owner_id in settings.EXCLUDED_OWNERS:
            logging.warning('owner excluded, skip: {}'.format(answer.url))
            continue

        question = cr.question(answer.question_id)
        if 'closed_date' in question.json:
            logging.warning('question closed, skip: {}'.format(answer.url))
            continue

        if answer and answer.score == 0:
            return [NARUTO_INTRO_MESSAGE, answer.url]


def send_message(room_id, message):
    email = settings.EMAIL
    password = settings.PASSWORD

    client = Client()
    client.login(email, password)
    client.send_message(room_id, message)


def parse_args():
    parser = ArgumentParser(description='RoboSanta CLI')
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-r', '--rooms', metavar='ROOMS', default=str(settings.ROOM_ID))
    parser.add_argument('--naruto', action='store_true', help='Post a Naruto answer')
    parser.add_argument('-m', '--message', help='Post a message in a chat room')

    args = parser.parse_args()

    if args.quiet:
        logging.basicConfig(level=logging.WARN)
    else:
        logging.basicConfig(level=logging.INFO)

    rooms = args.rooms.split(',')

    if args.message:
        messages = [args.message]
    elif args.naruto:
        messages = naruto()
    else:
        return

    if messages:
        for room_id in rooms:
            for message in messages:
                if not args.dry_run:
                    send_message(room_id, message)
                else:
                    logging.info('would send to {}: {}'.format(room_id, message))


def main():
    parse_args()


if __name__ == '__main__':
    main()

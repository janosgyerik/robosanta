#!/usr/bin/env python3

import logging
from argparse import ArgumentParser
import os

import random
from bs4 import BeautifulSoup
import requests
from stackexchange import CodeReview
from robosanta.stackexchange.chat.client import Client

from robosanta.stackexchange.data import queries
import settings


NARUTO_URL = 'http://data.stackexchange.com/codereview/query/264586/naruto-accepted-answer-with-zero-score'
NARUTO_INTRO_MESSAGE = 'hm, accepted answer with 0 score...'
NARUTO_CACHE = '.cache/naruto.html'


def main():
    parse_args()


def chat(args):
    send_message(args.room_id, args.message)


def naruto(args):
    logging.info('fetching Naruto posts')
    html = requests.get(NARUTO_URL).text
    soup = BeautifulSoup(html)

    def extract_answer_ids():
        data = queries.get_column(soup, 'Post Link')
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
            continue

        if answer and answer.score == 0:
            if not args.debug:
                send_message(args.room_id, NARUTO_INTRO_MESSAGE)
                send_message(args.room_id, answer.url)
            else:
                # logging.info('would send: {} <- {}'.format(args.room_id, NARUTO_INTRO_MESSAGE))
                logging.info('would send: {} <- {}'.format(args.room_id, answer.url))
            break


def parse_args():
    parser = ArgumentParser(description='RoboSanta CLI')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')

    subparsers = parser.add_subparsers(help='sub-command help')

    room_param_args = ('-r', '--room')
    room_param_kwargs = {'metavar': 'ROOM_ID', 'dest': 'room_id', 'default': settings.ROOM_ID}

    naruto_parser = subparsers.add_parser('naruto', help='Post a Naruto answer to The 2nd Monitor')
    naruto_parser.add_argument(*room_param_args, **room_param_kwargs)
    naruto_parser.set_defaults(func=naruto)

    chat_parser = subparsers.add_parser('chat', help='Post a message in a chat room')
    chat_parser.add_argument(*room_param_args, **room_param_kwargs)
    chat_parser.add_argument('message')
    chat_parser.set_defaults(func=chat)

    args = parser.parse_args()

    if args.quiet:
        logging.basicConfig(level=logging.WARN)
    else:
        logging.basicConfig(level=logging.INFO)

    args.func(args)


def send_message(room_id, message):
    email = settings.EMAIL
    password = settings.PASSWORD

    client = Client()
    client.login(email, password)
    client.send_message(room_id, message)


if __name__ == '__main__':
    main()

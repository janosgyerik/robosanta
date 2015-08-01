#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

import random
from bs4 import BeautifulSoup
import requests
from stackexchange import CodeReview
from robosanta.stackexchange.chat.client import Client

from robosanta.stackexchange.data import queries
import settings


NARUTO_URL = 'http://data.stackexchange.com/codereview/query/264586/naruto-accepted-answer-with-zero-score'


def main():
    logging.basicConfig(level=logging.INFO)
    parse_args()


def chat(args):
    send_message(args.room_id, args.message)


def naruto(args):
    logging.info('fetching naruto posts')
    data = requests.get(NARUTO_URL).text
    soup = BeautifulSoup(data)
    # with open(path) as fh:
    # soup = BeautifulSoup(fh)

    answer_ids = [value['id'] for value in queries.get_column(soup, 'Post Link')]
    random.shuffle(answer_ids)

    cr = CodeReview()
    for answer_id in answer_ids:
        try:
            logging.info('fetching answer {}'.format(answer_id))
            answer = cr.answer(answer_id)
        except ValueError:
            continue
        if answer and answer.score == 0:
            send_message(args.room_id, 'hm, accepted answer with 0 score... '
                                       'perhaps OP didn\'t have enough rep to upvote?')
            send_message(args.room_id, answer.url)
            break


def parse_args():
    parser = ArgumentParser(description='RoboSanta CLI')
    subparsers = parser.add_subparsers(help='sub-command help')

    room_param_args = ('-r', '--room')
    room_param_kwargs = {'metavar': 'ROOM_ID', 'dest': 'room_id', 'default': settings.ROOM_ID}

    naruto_parser = subparsers.add_parser('naruto', help='Post a Naruto answer to The 2nd Monitor')
    naruto_parser.add_argument(*room_param_args, **room_param_kwargs)
    naruto_parser.set_defaults(func=naruto)

    chat_parser = subparsers.add_parser('chat', help='Post a message in chat (debugging)')
    chat_parser.add_argument(*room_param_args, **room_param_kwargs)
    chat_parser.add_argument('message')
    chat_parser.set_defaults(func=chat)

    args = parser.parse_args()
    args.func(args)


def send_message(room_id, message):
    email = settings.EMAIL
    password = settings.PASSWORD

    client = Client()
    client.login(email, password)
    client.send_message(room_id, message)


if __name__ == '__main__':
    main()

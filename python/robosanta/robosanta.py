#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

import settings
from robosanta.plugins.code_only_answers import CodeOnlyAnswerPicker
from robosanta.plugins.naruto import NarutoPicker
from robosanta.plugins.ripe_zombie import RipeZombiePicker
from robosanta.stackexchange.chat.client import Client


def post_message(room_id, message):
    email = settings.EMAIL
    password = settings.PASSWORD

    client = Client()
    client.login(email, password)
    client.post_message(room_id, message)


def parse_args():
    parser = ArgumentParser(description='RoboSanta CLI')
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-r', '--rooms', metavar='ROOMS', default=str(settings.ROOM_IDS))
    parser.add_argument('--naruto', action='store_true', help='Post a Naruto answer')
    parser.add_argument('--ripe-zombie', action='store_true', help='Post a ripe zombie')
    parser.add_argument('--code-only-answer', action='store_true', help='Code-only answer')
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
        messages = NarutoPicker().pick()
    elif args.ripe_zombie:
        messages = RipeZombiePicker().pick()
    elif args.code_only_answer:
        messages = CodeOnlyAnswerPicker().pick()
    else:
        return

    if not messages:
        logging.info('no suitable messages found, exit')
        return

    for room_id in rooms:
        for message in messages:
            if not args.dry_run:
                post_message(room_id, message)
            else:
                logging.info('would post to {}: {}'.format(room_id, message))


def main():
    parse_args()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

from robosanta.stackexchange.chat.client import Client
import settings


def main():
    logging.basicConfig(level=logging.INFO)
    parse_args()


def chat(args):
    send_message(args.room_id, args.message)


def naruto(args):
    pass


def parse_args():
    parser = ArgumentParser(description='RoboSanta CLI')
    subparsers = parser.add_subparsers(help='sub-command help')

    naruto_parser = subparsers.add_parser('naruto', help='Post a Naruto answer to The 2nd Monitor')
    naruto_parser.add_argument('-r', '--room', metavar='ROOM_ID', default=settings.ROOM_ID)
    naruto_parser.set_defaults(func=naruto)

    chat_parser = subparsers.add_parser('chat', help='Post a message in chat (debugging)')
    chat_parser.add_argument('message')
    chat_parser.add_argument('-r', '--room', metavar='ROOM_ID', dest='room_id', default=settings.ROOM_ID)
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

#!/usr/bin/env python3

import logging
from datetime import datetime

from chatse.client import Client
import settings


def main():
    logging.basicConfig(level=logging.INFO)

    email = settings.EMAIL
    password = settings.PASSWORD
    room_id = settings.ROOM_ID

    client = Client()
    client.login(email, password)

    message = 'hello {}'.format(datetime.now())
    client.send_message(room_id, message)


if __name__ == '__main__':
    main()

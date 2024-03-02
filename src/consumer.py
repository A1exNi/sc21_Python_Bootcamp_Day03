import argparse
import logging
import redis
from threading import Thread
import json


def split_type(string: str):
    answer = []
    for num in string.split(','):
        answer.append(int(num))
    return answer


class ReadRedis(Thread):
    def __init__(self, bad_guys_numbers):
        super().__init__()
        if bad_guys_numbers:
            self.bad_guys_numbers = bad_guys_numbers
        else:
            self.bad_guys_numbers = []
        self.exit = False

    def get_string(self, message):
        d = json.loads(message['data'])
        if d['metadata']['to'] in self.bad_guys_numbers and d['amount'] > 0:
            d['metadata']['from'], d['metadata']['to'] = d['metadata']['to'], d['metadata']['from']
        return d

    def run(self):
        r = redis.Redis()
        p = r.pubsub(ignore_subscribe_messages=True)
        p.psubscribe('*')
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        while not self.exit:
            message = p.get_message()
            if message:
                string = self.get_string(message)
                logging.info(string)

    def stop(self):
        self.exit = True


def is_exit():
    s = input()
    if s == 'q':
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', type=split_type,
                        help='List of bad guys account numbers')
    args = parser.parse_args()
    reader = ReadRedis(args.e)
    reader.start()
    exit = False
    while not exit:
        exit = is_exit()
    reader.stop()


if __name__ == '__main__':
    main()

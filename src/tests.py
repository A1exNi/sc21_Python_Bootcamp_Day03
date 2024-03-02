from producer import get_message
from consumer import ReadRedis
import redis
import time
import logging


def test(account_from, account_to, amount, bad_guys):
    reader = ReadRedis(bad_guys)
    reader.start()
    r = redis.Redis()
    for i in range(len(account_from)):
        string = get_message(account_from[i], account_to[i], amount[i])
        time.sleep(0.1)
        r.publish('test', string)
    reader.stop()


def main():
    bad_guys = [1111111111, 2222222222]
    good_guys = [3333333333, 4444444444]
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.info('good guys:')
    logging.info(good_guys)
    logging.info('bad guys:')
    logging.info(bad_guys)
    logging.info('--------FROM GOOD TO GOOD--------')
    account_from = [good_guys[0], good_guys[0], good_guys[0]]
    account_to = [good_guys[1], good_guys[1], good_guys[1]]
    amount = [1000, -1000, 0]
    test(account_from, account_to, amount, bad_guys)
    logging.info('--------FROM GOOD TO BAD---------')
    account_from = [good_guys[0], good_guys[0], good_guys[0]]
    account_to = [bad_guys[1], bad_guys[1], bad_guys[1]]
    amount = [1000, -1000, 0]
    test(account_from, account_to, amount, bad_guys)
    logging.info('--------FROM BAD TO BAD----------')
    account_from = [bad_guys[0], bad_guys[0], bad_guys[0]]
    account_to = [bad_guys[1], bad_guys[1], bad_guys[1]]
    amount = [1000, -1000, 0]
    test(account_from, account_to, amount, bad_guys)
    logging.info('--------EMPTY BAD GUYS-----------')
    account_from = [good_guys[0], good_guys[0], good_guys[0]]
    account_to = [good_guys[1], good_guys[1], good_guys[1]]
    amount = [1000, -1000, 0]
    test(account_from, account_to, amount, [])
    account_from = [good_guys[0], good_guys[0], good_guys[0]]
    account_to = [bad_guys[1], bad_guys[1], bad_guys[1]]
    amount = [1000, -1000, 0]
    test(account_from, account_to, amount, [])
    account_from = [bad_guys[0], bad_guys[0], bad_guys[0]]
    account_to = [bad_guys[1], bad_guys[1], bad_guys[1]]
    amount = [1000, -1000, 0]
    test(account_from, account_to, amount, [])


if __name__ == '__main__':
    main()

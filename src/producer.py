import random
import redis
import logging
import json


def get_message(acconunt_from, account_to, amount):
    return json.dumps({
        'metadata': {
            'from': acconunt_from,
            'to': account_to
        },
        'amount': amount
    })


def gen_json(account_number: list[int], amount: list[int]):
    len_account_number = len(account_number)
    len_amount = len(amount)
    return get_message(
        account_number[random.randint(0, len_account_number - 1)],
        account_number[random.randint(0, len_account_number - 1)],
        amount[random.randint(0, len_amount - 1)]
    )


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    account_number = [1111111111, 2222222222, 3333333333, 4444444444,
                      5555555555]
    amount = [-10000, -5000, 0, 5000, 10000]
    string = gen_json(account_number, amount)
    logging.info(string)
    r = redis.Redis()
    r.publish('test', string)


if __name__ == '__main__':
    main()

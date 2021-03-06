import time

import requests
import json

from cryptoexchangecompare.celery import app

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from .models import Transaction, Account, ExchangeChoice, Status

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@app.task(name='get_orderbooks')
def get_orderbooks(coin):
    while True:
        nobitex_orderbook = json.loads(
            requests.get('https://api.nobitex.ir/v2/orderbook/' + str(coin).upper() + 'IRT').text)
        wallex_orderbook = json.loads(
            requests.get('https://api.wallex.ir/v1/depth?symbol=' + str(coin).upper() + 'TMN').text)
        phinix_orderbook = json.loads(
            requests.get('https://api.phinix.ir/v1/depth?symbol=' + str(coin).upper() + 'TMN').text)
        nobitex_bids = nobitex_orderbook['bids'][:5]
        nobitex_asks = nobitex_orderbook['asks'][:5]
        wallex_bids = wallex_orderbook['result']['bid'][:5]
        wallex_asks = wallex_orderbook['result']['ask'][:5]
        phinix_bids = phinix_orderbook['result']['bid'][:5]
        phinix_asks = phinix_orderbook['result']['ask'][:5]
        nobitex_bids = [{'price': float(bid[0]), 'quantity': float(bid[1]), 'exchange': 'Nobitex'} for bid in
                        nobitex_bids]
        nobitex_asks = [{'price': float(ask[0]), 'quantity': float(ask[1]), 'exchange': 'Nobitex'} for ask in
                        nobitex_asks]
        wallex_bids = [{'price': float(bid['price']), 'quantity': float(bid['quantity']), 'exchange': 'Wallex'} for
                       bid in wallex_bids]
        wallex_asks = [{'price': float(ask['price']), 'quantity': float(ask['quantity']), 'exchange': 'Wallex'} for
                       ask in wallex_asks]
        phinix_bids = [{'price': float(bid['price']), 'quantity': float(bid['quantity']), 'exchange': 'Phinix'} for
                       bid in phinix_bids]
        phinix_asks = [{'price': float(ask['price']), 'quantity': float(ask['quantity']), 'exchange': 'Phinix'} for
                       ask in phinix_asks]
        bids = (nobitex_bids + wallex_bids + phinix_bids)
        asks = (nobitex_asks + wallex_asks + phinix_asks)
        cache.set(str(coin).upper() + "bids", bids[:8], timeout=CACHE_TTL)
        cache.set(str(coin).upper() + "asks", asks[:8], timeout=CACHE_TTL)
        print('Data Saved')
        time.sleep(5)


@app.task(name='get_orderbook_from_exchange')
def get_orderbook_from_exchange(coin, exchange):
    while True:
        if exchange == 'nobitex':
            nobitex_orderbook = json.loads(
                requests.get('https://api.nobitex.ir/v2/orderbook/' + str(coin).upper() + 'IRT').text)
            nobitex_bids = nobitex_orderbook['bids'][:5]
            nobitex_asks = nobitex_orderbook['asks'][:5]
            nobitex_bids = [{'price': float(bid[0]), 'quantity': float(bid[1]), 'exchange': 'Nobitex'} for bid in
                            nobitex_bids]
            nobitex_asks = [{'price': float(ask[0]), 'quantity': float(ask[1]), 'exchange': 'Nobitex'} for ask in
                            nobitex_asks]
            cache.set(str(coin).upper() + exchange + 'bid', nobitex_bids, timeout=CACHE_TTL)
            cache.set(str(coin).upper() + exchange + 'ask', nobitex_asks, timeout=CACHE_TTL)
            print('Data Saved')
        else:
            orderbook = json.loads(
                requests.get(
                    'https://api.' + str(exchange).lower() + '.ir/v1/depth?symbol=' + str(coin).upper() + 'TMN').text)
            bids = orderbook['result']['bid'][:5]
            asks = orderbook['result']['ask'][:5]
            bids = [{'price': float(bid['price']), 'quantity': float(bid['quantity']), 'exchange': 'Wallex'} for
                    bid in bids]
            asks = [{'price': float(ask['price']), 'quantity': float(ask['quantity']), 'exchange': 'Wallex'} for
                    ask in asks]
            cache.set(str(coin).upper() + exchange + 'bid', bids, timeout=CACHE_TTL)
            cache.set(str(coin).upper() + exchange + 'ask', asks, timeout=CACHE_TTL)
            print('Data Saved')
        time.sleep(5)


@app.task(name='update_tokens')
def update_tokens():
    all_accounts = Account.objects.all()
    for account in all_accounts:
        if account.exchange == str(ExchangeChoice.NOBITEX):
            url = 'https://api.nobitex.ir/auth/login/'

            payload = json.dumps({
                'username': account.exchange_email,
                'password': account.exchange_password,
                "captcha": "api"
            })
            headers = {
                "Content-Type": "application/json"
            }

            response = requests.request("POST", url, headers=headers, data=payload).json()
            print(response)
            if 'status' in response and response['status'] == 'success':
                account.token = response['key']
                account.save()
        elif account.exchange == str(ExchangeChoice.PHINIX):
            url = "https://api.phinix.ir/auth/login"

            payload = json.dumps({
                "mobile_number": str(account.exchange_phone_number),
                "password": account.exchange_password
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload).json()
            if response['success']:
                account.token = response['result']['token']


@app.task(name='update_transactions_status')
def update_transactions_status():
    # Nobitex
    queryset = Transaction.objects.filter(exchange=ExchangeChoice.NOBITEX)
    for transaction in queryset:
        account = Account.objects.get(owner=transaction.customer, exchange=ExchangeChoice.NOBITEX)
        url = 'https://api.nobitex.ir/market/orders/status'

        payload = json.dumps({
            'id': transaction.transaction_id
        })
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Token " + account.token,
        }

        response = requests.request('POST', url, headers=headers, data=payload).json()
        if 'status' in response and response['status'] == 'ok':
            transaction.transaction_fee = float(response['order']['fee'])
            if response['order']['status'] == 'Active':
                transaction.status = Status.PENDING
            elif response['order']['status'] == 'Done':
                transaction.status = Status.SUCCESS
            elif response['order']['status'] == 'Canceled':
                transaction.status = Status.FAILED

    # Wallex
    queryset = Account.objects.filter(exchange=ExchangeChoice.WALLEX)
    for account in queryset:
        url = 'https://api.wallex.ir/v1/account/trades'
        payload = ""
        headers = {
            'Authorization': 'Bearer ' + account.token
        }

        response = requests.request('GET', url, headers=headers, data=payload).json()['AccountLatestTrades']
        user_transactions = Transaction.objects.filter(customer=account.owner, exchange=ExchangeChoice.WALLEX).\
            order_by('-created')
        counter = 0
        for transaction in response:
            if transaction['timestamp'] == str(user_transactions[counter].completion_date):
                counter += 1
                user_transactions[counter].transaction_fee = float(transaction['fee'])

        url = 'https://api.wallex.ir/v1/account/openOrders'
        payload = ""
        headers = {
            'Authorization': 'Bearer ' + account.token
        }

        response = requests.request('GET', url, headers=headers, data=payload).json()['result']['orders']
        user_transactions.update(status=Status.SUCCESS)
        for transaction in response:
            user_transactions.get(transaction_id=transaction['clientOrderId']).status = Status.PENDING

    # Phinix
    queryset = Account.objects.filter(exchange=ExchangeChoice.PHINIX)
    for account in queryset:
        url = 'https://api.phinix.ir/v1/account/trades'
        payload = ""
        headers = {
            'Authorization': 'Bearer ' + account.token
        }

        response = requests.request('GET', url, headers=headers, data=payload).json()['AccountLatestTrades']
        user_transactions = Transaction.objects.filter(customer=account.owner, exchange=ExchangeChoice.PHINIX). \
            order_by('-created')
        counter = 0
        for transaction in response:
            if transaction['timestamp'] == str(user_transactions[counter].completion_date):
                counter += 1
                user_transactions[counter].transaction_fee = float(transaction['fee'])

        url = 'https://api.phinix.ir/v1/account/openOrders'
        payload = ""
        headers = {
            'Authorization': 'Bearer ' + account.token
        }

        response = requests.request('GET', url, headers=headers, data=payload).json()['result']['orders']
        user_transactions.update(status=Status.SUCCESS)
        for transaction in response:
            user_transactions.get(transaction_id=transaction['clientOrderId']).status = Status.PENDING

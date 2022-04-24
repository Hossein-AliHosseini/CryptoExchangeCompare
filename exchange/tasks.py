import time

import requests
import json
from operator import itemgetter

from cryptoexchangecompare.celery import app

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from .models import Crypto

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

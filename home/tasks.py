import time

import requests
import json

from cryptoexchangecompare.celery import app

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@app.task(name='get_prices')
def get_prices():
    while True:
        nobitex_btc = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=btc&dstCurrency=rls').
                                 text)['stats']['btc-rls']['latest']
        nobitex_eth = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=eth&dstCurrency=rls').
                                 text)['stats']['eth-rls']['latest']
        nobitex_ada = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=ada&dstCurrency=rls').
                                 text)['stats']['ada-rls']['latest']
        nobitex_shib = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=shib&dstCurrency=rls').
                                  text)['stats']['shib-rls']['latest']
        nobitex_doge = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=doge&dstCurrency=rls').
                                  text)['stats']['doge-rls']['latest']

        wallex_market = json.loads(requests.get('https://api.wallex.ir/v1/markets').text)
        wallex_btc = wallex_market['result']['symbols']['BTCTMN']['stats']['lastPrice']
        wallex_eth = wallex_market['result']['symbols']['ETHTMN']['stats']['lastPrice']
        wallex_ada = wallex_market['result']['symbols']['ADATMN']['stats']['lastPrice']
        wallex_shib = wallex_market['result']['symbols']['SHIBTMN']['stats']['lastPrice']
        wallex_doge = wallex_market['result']['symbols']['DOGETMN']['stats']['lastPrice']

        phinix_market = json.loads(requests.get('https://api.phinix.ir/v1/markets').text)
        phinix_btc = phinix_market['result']['symbols']['BTCTMN']['stats']['lastPrice']
        phinix_eth = phinix_market['result']['symbols']['ETHTMN']['stats']['lastPrice']
        # phinix_ada = phinix_market['result']['symbols']['ADATMN']['stats']['lastPrice']
        # phinix_shib = phinix_market['result']['symbols']['SHIBTMN']['stats']['lastPrice']
        phinix_doge = phinix_market['result']['symbols']['DOGETMN']['stats']['lastPrice']

        cache.set('nobitex_btc', nobitex_btc, timeout=CACHE_TTL)
        cache.set('nobitex_eth', nobitex_eth, timeout=CACHE_TTL)
        cache.set('nobitex_ada', nobitex_ada, timeout=CACHE_TTL)
        cache.set('nobitex_shib', nobitex_shib, timeout=CACHE_TTL)
        cache.set('nobitex_doge', nobitex_doge, timeout=CACHE_TTL)
        cache.set('wallex_btc', wallex_btc, timeout=CACHE_TTL)
        cache.set('wallex_eth', wallex_eth, timeout=CACHE_TTL)
        cache.set('wallex_ada', wallex_ada, timeout=CACHE_TTL)
        cache.set('wallex_shib', wallex_shib, timeout=CACHE_TTL)
        cache.set('wallex_doge', wallex_doge, timeout=CACHE_TTL)
        cache.set('phinix_btc', phinix_btc, timeout=CACHE_TTL)
        cache.set('phinix_eth', phinix_eth, timeout=CACHE_TTL)
        cache.set('phinix_doge', phinix_doge, timeout=CACHE_TTL)
        print('Data Saved')
        time.sleep(5)

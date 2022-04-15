import requests
import json

from celery import shared_task


@shared_task
def get_prices():
    while True:
        nobitex_btc = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=btc&dstCurrency=rls',
                                              timeout=5).
                                 text)['stats']['btc-rls']['latest']
        nobitex_eth = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=eth&dstCurrency=rls',
                                              timeout=5).
                                 text)['stats']['eth-rls']['latest']
        nobitex_ada = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=ada&dstCurrency=rls',
                                              timeout=5).
                                 text)['stats']['ada-rls']['latest']
        nobitex_shib = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=shib&dstCurrency=rls',
                                              timeout=5).
                                  text)['stats']['shib-rls']['latest']
        nobitex_doge = json.loads(requests.get('https://api.nobitex.ir/market/stats?srcCurrency=doge&dstCurrency=rls',
                                              timeout=5).
                                  text)['stats']['doge-rls']['latest']

        wallex_market = json.loads(requests.get('https://api.wallex.ir/v1/markets', timeout=5).text)
        wallex_btc = wallex_market['result']['symbols']['BTCTMN']['stats']['lastPrice']
        wallex_eth = wallex_market['result']['symbols']['ETHTMN']['stats']['lastPrice']
        wallex_ada = wallex_market['result']['symbols']['ADATMN']['stats']['lastPrice']
        wallex_shib = wallex_market['result']['symbols']['SHIBTMN']['stats']['lastPrice']
        wallex_doge = wallex_market['result']['symbols']['DOGETMN']['stats']['lastPrice']

        phinix_market = json.loads(requests.get('https://api.phinix.ir/v1/markets', timeout=5).text)
        phinix_btc = phinix_market['result']['symbols']['BTCTMN']['stats']['lastPrice']
        phinix_eth = phinix_market['result']['symbols']['ETHTMN']['stats']['lastPrice']
        # phinix_ada = phinix_market['result']['symbols']['ADATMN']['stats']['lastPrice']
        # phinix_shib = phinix_market['result']['symbols']['SHIBTMN']['stats']['lastPrice']
        phinix_doge = phinix_market['result']['symbols']['DOGETMN']['stats']['lastPrice']

        cache = open('prices.txt', 'w+')
        cache.write(nobitex_btc + '\n' +
                    nobitex_eth + '\n' +
                    nobitex_ada + '\n' +
                    nobitex_shib + '\n' +
                    nobitex_doge + '\n' +
                    wallex_btc + '\n' +
                    wallex_eth + '\n' +
                    wallex_ada + '\n' +
                    wallex_shib + '\n' +
                    wallex_doge + '\n' +
                    phinix_btc + '\n' +
                    phinix_eth + '\n' +
                    phinix_doge)
        cache.close()

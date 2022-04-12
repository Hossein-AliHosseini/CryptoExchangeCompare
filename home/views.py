from django.shortcuts import render
from django.conf import settings
import requests
import json


def home_page(request):
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

    return render(request, 'home_page/home_page.html', {'nobitex_btc': nobitex_btc,
                                                        'nobitex_eth': nobitex_eth,
                                                        'nobitex_ada': nobitex_ada,
                                                        'nobitex_shib': nobitex_shib,
                                                        'nobitex_doge': nobitex_doge,
                                                        'wallex_btc': wallex_btc,
                                                        'wallex_eth': wallex_eth,
                                                        'wallex_ada': wallex_ada,
                                                        'wallex_shib': wallex_shib,
                                                        'wallex_doge': wallex_doge,
                                                        'phinix_btc': phinix_btc,
                                                        'phinix_eth': phinix_eth,
                                                        # 'phinix_ada': phinix_ada,
                                                        # 'phinix_shib': phinix_shib,
                                                        'phinix_doge': phinix_doge,
                                                        'BTC_URL': settings.MEDIA_URL + 'coins/btc.png',
                                                        'ETH_URL': settings.MEDIA_URL + 'coins/eth.png',
                                                        'ADA_URL': settings.MEDIA_URL + 'coins/ada.png',
                                                        'DOGE_URL': settings.MEDIA_URL + 'coins/doge.png',
                                                        'SHIB_URL': settings.MEDIA_URL + 'coins/shib.png',
                                                        })

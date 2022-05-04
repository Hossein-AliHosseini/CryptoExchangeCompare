from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache


def get_offer(coin):
    nobitex = float(cache.get('nobitex_' + coin))
    wallex = float(cache.get('wallex_' + coin))
    phinix = float(cache.get('phinix_' + coin))
    _list = [nobitex, wallex, phinix]
    _min, _max = min(_list), max(_list)
    _diff = _max - _min
    min_index, max_index = _list.index(_min), _list.index(_max)

    if min_index == 0:
        _min = 'Nobitex: ' + str(_min)
    elif min_index == 1:
        _min = 'Wallex: ' + str(_min)
    else:
        _min = 'Phinix: ' + str(_min)

    if max_index == 0:
        _max = 'Nobitex: ' + str(_max)
    elif max_index == 1:
        _max = 'Wallex: ' + str(_max)
    else:
        _max = 'Phinix: ' + str(_max)

    return _min, _max, _diff


def home_page(request):
    btc_min, btc_max, btc_diff = get_offer('btc')
    eth_min, eth_max, eth_dif = get_offer('eth')
    doge_min, doge_max, doge_diff = get_offer('doge')

    return render(request, 'home_page/home_page.html', {'nobitex_btc': cache.get('nobitex_btc'),
                                                        'nobitex_eth': cache.get('nobitex_eth'),
                                                        'nobitex_ada': cache.get('nobitex_ada'),
                                                        'nobitex_shib': cache.get('nobitex_shib'),
                                                        'nobitex_doge': cache.get('nobitex_doge'),
                                                        'wallex_btc': cache.get('wallex_btc'),
                                                        'wallex_eth': cache.get('wallex_eth'),
                                                        'wallex_ada': cache.get('wallex_ada'),
                                                        'wallex_shib': cache.get('wallex_shib'),
                                                        'wallex_doge': cache.get('wallex_doge'),
                                                        'phinix_btc': cache.get('phinix_btc'),
                                                        'phinix_eth': cache.get('phinix_eth'),
                                                        # 'phinix_ada': phinix_ada,
                                                        # 'phinix_shib': phinix_shib,
                                                        'phinix_doge': cache.get('phinix_doge'),
                                                        'btc_min': btc_min,
                                                        'btc_max': btc_max,
                                                        'btc_diff': btc_diff,
                                                        'eth_min': eth_min,
                                                        'eth_max': eth_max,
                                                        'eth_diff': eth_dif,
                                                        'doge_min': doge_min,
                                                        'doge_max': doge_max,
                                                        'doge_diff': doge_diff,
                                                        'BTC_URL': settings.MEDIA_URL + 'coins/btc.png',
                                                        'ETH_URL': settings.MEDIA_URL + 'coins/eth.png',
                                                        'ADA_URL': settings.MEDIA_URL + 'coins/ada.png',
                                                        'DOGE_URL': settings.MEDIA_URL + 'coins/doge.png',
                                                        'SHIB_URL': settings.MEDIA_URL + 'coins/shib.png',
                                                        })

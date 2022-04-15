from django.shortcuts import render
from django.conf import settings


def home_page(request):
    cache = open('prices.txt', 'r')
    cache = cache.read().split('\n')
    while cache is not None:
        return render(request, 'home_page/home_page.html', {'nobitex_btc': cache[0],
                                                            'nobitex_eth': cache[1],
                                                            'nobitex_ada': cache[2],
                                                            'nobitex_shib': cache[3],
                                                            'nobitex_doge': cache[4],
                                                            'wallex_btc': cache[5],
                                                            'wallex_eth': cache[6],
                                                            'wallex_ada': cache[7],
                                                            'wallex_shib': cache[8],
                                                            'wallex_doge': cache[9],
                                                            'phinix_btc': cache[10],
                                                            'phinix_eth': cache[11],
                                                            # 'phinix_ada': phinix_ada,
                                                            # 'phinix_shib': phinix_shib,
                                                            'phinix_doge': cache[12],
                                                            'BTC_URL': settings.MEDIA_URL + 'coins/btc.png',
                                                            'ETH_URL': settings.MEDIA_URL + 'coins/eth.png',
                                                            'ADA_URL': settings.MEDIA_URL + 'coins/ada.png',
                                                            'DOGE_URL': settings.MEDIA_URL + 'coins/doge.png',
                                                            'SHIB_URL': settings.MEDIA_URL + 'coins/shib.png',
                                                            })

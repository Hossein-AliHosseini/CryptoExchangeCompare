from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache


def home_page(request):
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
                                                        'BTC_URL': settings.MEDIA_URL + 'coins/btc.png',
                                                        'ETH_URL': settings.MEDIA_URL + 'coins/eth.png',
                                                        'ADA_URL': settings.MEDIA_URL + 'coins/ada.png',
                                                        'DOGE_URL': settings.MEDIA_URL + 'coins/doge.png',
                                                        'SHIB_URL': settings.MEDIA_URL + 'coins/shib.png',
                                                        })

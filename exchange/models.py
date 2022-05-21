from django.db import models

from model_utils.models import TimeStampedModel

from user.models import User


class ExchangeChoice:
    NOBITEX = 'Nobitex'
    WALLEX = 'Wallex'
    PHINIX = 'Phinix'
    EXIR = 'Exir'

    TYPES = (
        (NOBITEX, 'Nobitex'),
        (WALLEX, 'Wallex'),
        (PHINIX, 'Phinix'),
        (EXIR, 'Exir'),
    )


class Crypto:
    BITCOIN = 'BTC'
    ETHEREUM = 'ETH'
    SHIBA = 'SHIB'
    CARDANO = 'ADA'
    DOGECOIN = 'DOGE'
    TETHER = "USDT"

    TYPES = (
        (BITCOIN, 'BTC'),
        (ETHEREUM, 'ETH'),
        (SHIBA, 'SHIB'),
        (CARDANO, 'ADA'),
        (DOGECOIN, 'DOGE'),
        (TETHER, 'USDT'),
    )


class Status:
    PENDING = 'Pending'
    FAILED = 'Failed'
    SUCCESS = 'Success'
    TYPES = (
        (PENDING, 'Pending'),
        (FAILED, 'Failed'),
        (SUCCESS, 'Success'),
    )


class TransactionType:
    BUY = 'Buy'
    SELL = 'Sell'
    TYPES = (
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    )


class ExchangeProvider(TimeStampedModel):
    name = models.CharField(max_length=16,
                            default=ExchangeChoice.NOBITEX,
                            choices=ExchangeChoice.TYPES,)
    obtain_token_command = models.CharField(max_length=256,
                                            null=True, blank=True)
    place_bid_command = models.CharField(max_length=256,
                                         null=True, blank=True)
    get_assets_command = models.CharField(max_length=256,
                                          null=True, blank=True)
    get_market_details_command = models.CharField(max_length=256,
                                                  null=True, blank=True)


class Account(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='account')
    exchange = models.CharField(max_length=10,
                                choices=ExchangeChoice.TYPES,
                                default=ExchangeChoice.NOBITEX)
    token = models.CharField(max_length=128, blank=True)
    wallet_address = models.CharField(max_length=128, blank=True)
    exchange_email = models.EmailField(max_length=128, null=True)
    exchange_phone_number = models.CharField(max_length=32, null=True)
    exchange_password = models.CharField(max_length=128, null=True)

    class Meta:
        unique_together = ('owner', 'exchange')

    def __str__(self):
        return str(self.exchange) + ' Account with Email: ' + str(self.exchange_email) + ' and Phone Number: ' + str(self.exchange_phone_number)


class Transaction(TimeStampedModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='transaction')
    dual_transaction = models.OneToOneField('exchange.Transaction', on_delete=models.CASCADE,
                                            related_name='dual', null=True)
    crypto = models.CharField(max_length=6,
                              choices=Crypto.TYPES,
                              default=Crypto.BITCOIN)
    exchange = models.CharField(max_length=10,
                                choices=ExchangeChoice.TYPES,
                                default=ExchangeChoice.NOBITEX)
    status = models.CharField(max_length=16,
                              choices=Status.TYPES,)
    completion_date = models.DateTimeField(null=True)
    type = models.CharField(max_length=8,
                            choices=TransactionType.TYPES,
                            null=True)
    transaction_fee = models.FloatField()
    size = models.FloatField()
    price = models.FloatField()
    stop_limit = models.FloatField(blank=True, null=True)
    transaction_id = models.CharField(max_length=256)

    def __str__(self):
        return str(self.type) + ' ' + str(self.size) + ' ' + str(self.crypto) + ' in ' + str(self.exchange) + ' for ' + str(self.price) + ' Tether (Status: ' + str(self.status) + ')'

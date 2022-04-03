from django.db import models

from model_utils.models import TimeStampedModel

from user.models import User


class Exchange:
    NOBITEX = 'Nobitex'
    WALLEX = 'Wallex'
    PHINIX = 'Phinix'

    TYPES = (
        (NOBITEX, 'Nobitex'),
        (WALLEX, 'Wallex'),
        (PHINIX, 'Phinix'),
    )


class Crypto:
    BITCOIN = 'BTC'
    ETHERRUM = 'ETH'
    SHIBA = 'SHIB'
    CARDANO = 'ADA'
    TRON = 'TRX'
    DOGECOIN = 'DOGE'

    TYPES = (
        (BITCOIN, 'BTC'),
        (ETHERRUM, 'ETH'),
        (SHIBA, 'SHIB'),
        (CARDANO, 'ADA'),
        (TRON, 'TRX'),
        (DOGECOIN, 'DOGE'),
    )


class Status:
    NEW = 'New'
    PENDING = 'Pending'
    FAILED = 'Failed'
    SUCCESS = 'Success'
    TYPES = (
        (NEW, 'New'),
        (PENDING, 'Pending'),
        (FAILED, 'Failed'),
        (SUCCESS, 'Success'),
    )


class Account(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='account')
    exchange = models.CharField(max_length=10,
                                choices=Exchange.TYPES,
                                default=Exchange.NOBITEX)
    token = models.CharField(max_length=128, null=True)

    class Meta:
        unique_together = ('owner', 'exchange')


class Transaction(TimeStampedModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='transaction')
    crypto = models.CharField(max_length=6,
                              choices=Crypto.TYPES,
                              default=Crypto.BITCOIN)
    exchange = models.CharField(max_length=10,
                                choices=Exchange.TYPES,
                                default=Exchange.NOBITEX)
    status = models.CharField(max_length=16,
                              choices=Status.TYPES,)
    volume = models.FloatField()
    size = models.FloatField()
    price = models.FloatField()

import os

import django

from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cryptoexchangecompare.settings.development')
django.setup()

from user.models import User, Person
from exchange.models import Account, Transaction, ExchangeChoice, Crypto, Status, TransactionType


def create_user():
    User.objects.all().delete()
    fake = Faker()
    for _ in range(20):
        sample_user = User.objects.create(
            email=fake.email(),
            username=fake.user_name(),
            # is_active=False,
        )
        sample_user.set_password('fakePassword')
        sample_user.save()
        sample_person = Person.objects.create(
            user=sample_user,
            phone_number=fake.phone_number(),
            national_code=fake.random_int(min=1000000000, max=9999999999),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.address(),
            birthdate=fake.date_of_birth(),
        )
        sample_person.save()


def create_account():
    Account.objects.all().delete()
    fake = Faker()
    for _ in range(20):
        sample_account = Account.objects.create(
            owner=User.objects.all()[_],
            exchange=ExchangeChoice.NOBITEX if _ % 2 == 0 else ExchangeChoice.WALLEX,
            token=fake.pystr(),
            wallet_address=fake.pystr(),
            exchange_email=fake.email(),
            exchange_phone_number=fake.phone_number(),
            exchange_password=fake.pystr()
        )
        sample_account.save()


def create_transaction():
    Transaction.objects.all().delete()
    fake = Faker()
    for _ in range(20):
        sample_transaction = Transaction.objects.create(
            customer=User.objects.all()[_],
            type=TransactionType.BUY if _ % 2 == 0 else TransactionType.SELL,
            base_crypto=Crypto.BITCOIN if _ % 2 == 0 else Crypto.ETHEREUM,
            quote_crypto=Crypto.ETHEREUM if _ % 2 == 0 else Crypto.TETHER,
            exchange=ExchangeChoice.NOBITEX if _ % 2 == 0 else ExchangeChoice.PHINIX,
            tether_equivalent=fake.pyfloat(positive=True),
            status=Status.PENDING if _ % 2 == 0 else Status.SUCCESS,
            completion_date=fake.date_time(),
            volume=fake.pyfloat(positive=True),
            size=fake.pyfloat(positive=True),
            price=fake.pyfloat(positive=True)
        )
        sample_transaction.save()
    for _ in range(0, 20, 2):
        Transaction.objects.all()[_].opposite_transaction = Transaction.objects.all()[_+1]
        Transaction.objects.all()[_+1].opposite_transaction = Transaction.objects.all()[_]


create_user()
create_account()
create_transaction()

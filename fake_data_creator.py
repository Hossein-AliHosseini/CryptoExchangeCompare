import os

import django

from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cryptoexchangecompare.settings.development')
django.setup()

from user.models import User, Person
from exchange.models import Account, Transaction, Exchange, Crypto, Status


def create_user():
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
    fake = Faker()
    for _ in range(20):
        sample_account = Account.objects.create(
            owner=User.objects.all()[_],
            exchange=Exchange.NOBITEX if _ % 2 == 0 else Exchange.WALLEX,
            token=fake.pystr()
        )
        sample_account.save()


def create_transaction():
    fake = Faker()
    for _ in range(20):
        sample_transaction = Transaction.objects.create(
            customer=User.objects.all()[_],
            crypto=Crypto.BITCOIN if _ % 2 == 0 else Crypto.ETHERRUM,
            exchange=Exchange.NOBITEX if _ % 2 == 0 else Exchange.PHINIX,
            status=Status.PENDING if _ % 2 == 0 else Status.SUCCESS,
            volume=fake.random_int(min=0, max=5),
            size=fake.random_int(min=0, max=60000),
            price=fake.random_int(min=0, max=10000000)
        )
        sample_transaction.save()


create_user()
create_account()
create_transaction()

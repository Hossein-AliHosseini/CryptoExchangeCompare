import django_tables2 as tables

from .models import Transaction, Account


class TransactionTable(tables.Table):
    class Meta:
        exclude = ['id', 'modified']
        model = Transaction
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no Transaction to show...'


class AccountTable(tables.Table):
    class Meta:
        model = Account
        exclude = ['owner', 'modified', 'id', 'exchange_password']
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no Account to show...'


class OrderbookTable(tables.Table):
    price = tables.Column(verbose_name='Price')
    quantity = tables.Column(verbose_name='Quantity')
    exchange = tables.Column(verbose_name='Exchange')

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no order to show'

    def render_price(self, value):
        return value

    def render_quantity(self, value):
        return value

    def render_exchange(self, value):
        return value

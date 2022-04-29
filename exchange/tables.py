import django_tables2 as tables
from django_tables2.utils import A

from .models import Transaction, Account


class TransactionTable(tables.Table):
    dual_price = tables.Column(accessor='dual_transaction.price',
                               verbose_name='Dual transaction price')

    class Meta:
        exclude = ['modified', 'customer', ]
        model = Transaction
        order_by = 'completion_date'
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no Transaction to show...'
        row_attrs = {"TYPE": lambda record: record.type}


class AccountTable(tables.Table):
    edit = tables.LinkColumn(viewname='edit_account', text="Edit", args=[A('pk')])

    class Meta:
        model = Account
        exclude = ['owner', 'modified', 'id', 'exchange_password']
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no Account to show...'


class BidsTable(tables.Table):
    price = tables.Column(verbose_name='Price')
    quantity = tables.Column(verbose_name='Quantity')
    exchange = tables.Column(verbose_name='Exchange')

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no order to show'
        row_attrs = {"style": lambda record: "background-color: #8b3636;"}

    def render_price(self, value):
        return value

    def render_quantity(self, value):
        return value

    def render_exchange(self, value):
        return value


class AsksTable(tables.Table):
    price = tables.Column(verbose_name='Price')
    quantity = tables.Column(verbose_name='Quantity')
    exchange = tables.Column(verbose_name='Exchange')

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no order to show'
        row_attrs = {"style": lambda record: "background-color: #528b47;"}

    def render_price(self, value):
        return value

    def render_quantity(self, value):
        return value

    def render_exchange(self, value):
        return value

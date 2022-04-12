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
        exclude = ['token', 'owner', 'modified', 'id']
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no Account to show...'

import django_tables2 as tables

from exchange.models import Transaction, Account


class TransactionsReportTable(tables.Table):
    class Meta:
        models = Transaction
        exclude = ('id',)


class AccountsReportTable(tables.Table):
    class Meta:
        model = Account
        exclude = ('id',)
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no Account to show...'

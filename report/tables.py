import django_tables2 as tables
from django_tables2.export.views import ExportMixin

from exchange.models import Transaction, Account
from user.models import User


class TransactionsReportTable(tables.Table):
    class Meta:
        models = Transaction
        exclude = ('id',)


class AccountsReportTable(tables.Table):
    class Meta:
        model = Account
        exclude = ('id', 'token', 'wallet_address', 'modified')
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no Account to show...'


class AccountTableView(ExportMixin, tables.SingleTableView):
    table_class = TransactionsReportTable
    model = Account
    template_name = 'django_tables2/bootstrap4.html'


class UsersReportTable(tables.Table):

    class Meta:
        model = User
        fields = ('email', 'username', 'accounts', 'transactions',
                  'last_login', 'is_superuser', 'is_active', 'date_joined')
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'There is no Data to show...'

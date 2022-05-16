from django.shortcuts import render

from .models import ReportType
from .forms import ReportForm
from .tables import TransactionsReportTable, AccountsReportTable
from .filters import TransactionFilter, AccountFilter
from exchange.models import Transaction, Account


def dt_report(request):
    # if request.method == 'POST':
    #     form = ReportForm(request.POST)
    #     user = form.cleaned_data['user']
    #     display_field = form.cleaned_data['display_field']
    #     if display_field == str(ReportType.TRANSACTIONS):
    #         queryset = Transaction.objects.all()
    #         if user is not None:
    #             queryset.filter(customer=user)
    #         filter = TransactionFilter(request.POST, queryset=queryset)
    #         table = TransactionsReportTable(queryset)
    #     else:
    #         queryset = Account.objects.all(owner=user)
    #         if user is not None:
    #             queryset.filter(owner=user)
    #         filter = AccountFilter(request.POST, queryset=queryset)
    #         table = AccountsReportTable(queryset)
    #     table.paginate(page=request.GET.get('page', 1), per_page=10)
    # else:
        # form = ReportForm()
        # table = {}
    filter = AccountFilter(request.GET, queryset=Account.objects.all())
    table = AccountsReportTable(filter.qs)
    return render(request, 'report/django_table_report.html',
                  {'filter': filter, 'table': table})


def ht_report(request):
    filter = TransactionFilter(request.GET, queryset=Transaction.objects.all())
    return render(request, 'report/html_table_report.html',
                  {'filter': filter})

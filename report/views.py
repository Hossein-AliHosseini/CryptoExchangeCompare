import json

from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from django.core.cache import cache

from .tables import AccountsReportTable, UsersReportTable
from .filters import TransactionFilter, AccountFilter, UserFilter
from exchange.models import Transaction, Account
from user.models import User
from .tasks import download_table, download_xls

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
import xlwt


def dt_report(request):
    filter = AccountFilter(request.GET, queryset=Account.objects.all())
    table = AccountsReportTable(filter.qs)

    RequestConfig(request).configure(table)
    export_format = request.GET.get("_export", None)

    if export_format:
        res = download_table.delay(export_format,
                                   list(filter.qs.values_list('id', flat=True)))
        if res.get() == 'blp':
            return cache.get('blp')

    return render(request, 'report/django_table_report.html',
                  {'filter': filter, 'table': table})


def ht_report(request):
    filter = TransactionFilter(request.GET, queryset=Transaction.objects.all())
    queryset = filter.qs

    export_format = request.GET.get("_export", None)
    if export_format:
        res = download_xls.delay(list(queryset.values_list('id', flat=True)))

        if res.get() == 'dlp':
            return cache.get('dlp')

    return render(request, 'report/html_table_report.html',
                  {'filter': filter})


def cumulative_report(request):
    # queryset = User.objects.all()
    start_date = request.GET.get('date_joined__date__gte', None)
    end_date = request.GET.get('date_joined__date__lte', None)
    filter = UserFilter(request.GET, queryset=User.objects.all())
    queryset = filter.qs
    if start_date:
        queryset = queryset.filter(date_joined__date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date_joined__date__lte=end_date)
    queryset = filter.qs.annotate(
        accounts=F('account'), transactions=F('transaction')).values()

    for query in queryset:
        if query['transactions']:
            query['transactions'] = Transaction.objects.get(pk=query['transactions'])
        if query['accounts']:
            query['accounts'] = Account.objects.get(pk=query['accounts'])

    table = UsersReportTable(queryset)
    print(queryset[0]['accounts'].owner)

    RequestConfig(request).configure(table)
    export_format = request.GET.get("_export", None)

    if export_format:
        res = download_table.delay(export_format,
                                   list(filter.qs.values_list('id', flat=True)))
        if res.get() == 'blp':
            return cache.get('blp')

    return render(request, 'report/cumulative_report.html',
                  {'filter': filter, 'table': table})

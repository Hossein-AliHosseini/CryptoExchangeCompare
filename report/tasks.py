from cryptoexchangecompare.celery import app

from django.core import serializers
from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport

from .tables import AccountsReportTable, UsersReportTable
from exchange.models import Account, Transaction
from user.models import User

import xlwt


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@app.task(name='download_table')
def download_table(export_format, queryset):
    queryset = Account.objects.filter(id__in=queryset)
    table = UsersReportTable(queryset)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        cache.set('blp', exporter.response("table.{}".format(export_format)), timeout=CACHE_TTL)
        return 'blp'
    else:
        return 'Wrong Format...'


@app.task(name='download_xls_t')
def download_xls_t(rows):
    # queryset = Transaction.objects.filter(id__in=queryset)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="table.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Transactions')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        'Created',
        'Customer',
        'Crypto',
        'Exchange',
        'Status',
        'Type',
        'Transaction Fee',
        'Size',
        'Price',
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    # rows = queryset.values_list('created', 'customer', 'crypto',
    #                             'exchange', 'status', 'type',
    #                             'transaction_fee',
    #                             'size', 'price')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    cache.set('tlp', response, timeout=CACHE_TTL)
    return 'tlp'


@app.task(name='download_xls_a')
def download_xls_a(rows):
    # queryset = Account.objects.filter(id__in=queryset)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="table.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Accounts')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        'Owner',
        'Created',
        'Exchange',
        'Exchange Email',
        'Exchange Phone Number',
        'Exchange Password',
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    # rows = queryset.values_list('owner', 'created',
    #                             'exchange', 'exchange_email',
    #                             'exchange_phone_number',
    #                             'exchange_password')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    cache.set('alp', response, timeout=CACHE_TTL)
    return 'alp'


@app.task(name='download_xls_u')
def download_xls_u(rows):
    # queryset = User.objects.filter(id__in=queryset)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="table.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        'Email',
        'Username',
        'Accounts',
        'Transactions',
        'Last Login',
        'Superuser Status',
        'Active',
        'Date Joined'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    # rows = queryset.values_list('email', 'username',
    #                             'account', 'transaction',
    #                             'last_login', 'is_superuser',
    #                             'is_active',
    #                             'date_joined')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    # file = open('table.xls', 'w')
    # file.write(response)
    # file.close()
    cache.set('ulp', response, timeout=CACHE_TTL)
    return 'ulp'

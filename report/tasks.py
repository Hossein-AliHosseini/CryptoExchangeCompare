from cryptoexchangecompare.celery import app

from django.core import serializers
from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport

from .tables import AccountsReportTable
from exchange.models import Account, Transaction

import xlwt


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@app.task(name='download_table')
def download_table(export_format, queryset):
    print('blp')
    queryset = Account.objects.filter(id__in=queryset)
    table = AccountsReportTable(queryset)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        cache.set('blp', exporter.response("table.{}".format(export_format)), timeout=CACHE_TTL)
        return 'blp'
    else:
        return 'Wrong Format...'


@app.task(name='download_xls')
def download_xls(queryset):
    queryset = Transaction.objects.filter(id__in=queryset)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="table.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Transactions')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
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

    rows = queryset.values_list('customer', 'crypto',
                                'exchange', 'status', 'type',
                                'transaction_fee',
                                'size', 'price')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    cache.set('dlp', response, timeout=CACHE_TTL)
    return 'dlp'

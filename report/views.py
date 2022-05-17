from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse

from .models import ReportType
from .forms import ReportForm
from .tables import TransactionsReportTable, AccountsReportTable
from .filters import TransactionFilter, AccountFilter
from exchange.models import Transaction, Account

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from openpyxl import Workbook
import xlwt


def dt_report(request):
    filter = AccountFilter(request.GET, queryset=Account.objects.all())
    table = AccountsReportTable(filter.qs)

    RequestConfig(request).configure(table)
    export_format = request.GET.get("_export", None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    return render(request, 'report/django_table_report.html',
                  {'filter': filter, 'table': table,
                   'domain': '127.0.0.1:8000/report/dt_report'})


def ht_report(request):
    filter = TransactionFilter(request.GET, queryset=Transaction.objects.all())
    queryset = filter.qs
    export_format = request.GET.get("_export", None)
    if export_format:
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
        print(rows)
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response
    return render(request, 'report/html_table_report.html',
                  {'filter': filter})

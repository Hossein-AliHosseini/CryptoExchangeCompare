import json

from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Q
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.urls import resolve

from .tables import AccountsReportTable, UsersReportTable
from .filters import TransactionFilter, AccountFilter, UserFilter
from exchange.models import Transaction, Account
from user.models import User
from .tasks import download_xls_t, download_xls_a, download_xls_u

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from dal import autocomplete
import xlwt
from celery.result import AsyncResult


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def dt_report(request):
    url = request.build_absolute_uri()
    if '?' in url:
        url += '&_export=xlsx'
    else:
        url += '?_export=xlsx'
    filter = AccountFilter(request.GET, queryset=Account.objects.all())
    queryset = filter.qs
    table = AccountsReportTable(queryset)

    export_format = request.GET.get("_export", None)

    if export_format:
        res = download_xls_a.delay(list(queryset.values_list('owner__username', 'created',
                                                             'exchange', 'exchange_email',
                                                             'exchange_phone_number',
                                                             'exchange_password')))

        return render(request, 'report/django_table_report.html',
                      {'filter': filter, 'table': table,
                       'task_id': res.task_id,
                       'url': url})
    return render(request, 'report/django_table_report.html',
                  {'filter': filter, 'table': table, 'url': url})


def ht_report(request):
    url = request.build_absolute_uri()
    if '?' in url:
        url += '&_export=xlsx'
    else:
        url += '?_export=xlsx'
    filter = TransactionFilter(request.GET, queryset=Transaction.objects.all())
    queryset = filter.qs

    export_format = request.GET.get("_export", None)
    if export_format:
        # cache.set("request", request, timeout=CACHE_TTL)
        res = download_xls_t.delay(list(queryset.values_list('created', 'customer__username', 'crypto',
                                                             'exchange', 'status', 'type',
                                                             'transaction_fee',
                                                             'size', 'price')))

        # todo:
        # if res.get() == 'tlp':
        #     return cache.get('tlp')

        return render(request, 'report/html_table_report.html',
                    {'filter': filter, 'task_id': res.task_id,
                     'url': url})
    return render(request, 'report/html_table_report.html',
                  {'filter': filter, 'url': url})


def cumulative_report(request):
    url = request.build_absolute_uri()
    if '?' in url:
        url += '&_export=xlsx'
    else:
        url += '?_export=xlsx'
    print(url)
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

    blpp = list()
    for query in queryset:
        if query['transactions']:
            query['transactions'] = str(Transaction.objects.get(pk=query['transactions']))
        if query['accounts']:
            query['accounts'] = str(Account.objects.get(pk=query['accounts']))
        blpp.append((query['email'], query['username'], query['accounts'], query['transactions'],
                     query['last_login'], query['is_superuser'], query['is_active'], query['date_joined'],))

    table = UsersReportTable(queryset)
    # has_filter = any(field in request.GET for field in set(f.get_fields()))

    RequestConfig(request).configure(table)
    # cache.set('table', table, timeout=CACHE_TTL)

    export_format = request.GET.get("_export", None)

    if export_format:
        res = download_xls_u.delay(blpp)
        # # todo:
        # if res.get() == 'ulp':
        #     return cache.get('ulp')

        return render(request, 'report/cumulative_report.html',
                      {'filter': filter, 'table': table,
                       'queryset': User.objects.all(),
                       'task_id': res.task_id, 'url': url})
    return render(request, 'report/cumulative_report.html',
                  {'filter': filter, 'table': table,
                   'queryset': User.objects.all(), 'url': url})


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()

        if self.q:
            qs = qs.filter(email__icontains=self.q)
        return qs


def email_autocomplete(request):
    # if request.is_ajax():
    q = request.GET.get('term', '')
    res = list()
    queryset = User.objects.filter(email__icontains=q)
    for query in queryset:
        res.append(query.email)
    data = json.dumps(res)
    mimetypes = 'application/json'
    return HttpResponse(data, mimetypes)


def username_autocomplete(request):
    q = request.GET.get('term', '')
    res = list()
    queryset = User.objects.filter(username__icontains=q)
    for query in queryset:
        res.append(query.username)
    data = json.dumps(res)
    mimetypes = 'application/json'
    return HttpResponse(data, mimetypes)


def check_status(request):
    task_id = request.GET.get('task_id')
    status = AsyncResult(task_id)
    if status.ready():
        return cache.get(status.get())
    else:
        return False

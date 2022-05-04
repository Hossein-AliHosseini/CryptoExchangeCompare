from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.core.cache import cache

from .tables import TransactionTable, AccountTable, AsksTable, BidsTable
from .models import Transaction, Account, TransactionType, Status, ExchangeChoice
from .forms import AccountForm, ProfitAndLossForm, ChoiceExchangeForm,\
    TradeForm, ChoiceForm, WithdrawForm, WithdrawConfirmForm

import requests
import json


def transaction_view(request):
    if request.user.is_authenticated:
        queryset = Transaction.objects.filter(customer=request.user)
        table = TransactionTable(queryset)
        table.paginate(page=request.GET.get('page', 1), per_page=10)
        return render(request, 'exchange/transactions.html', {'table': table})
    else:
        return HttpResponse('Please login first...')


def exchange_account_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    else:
        queryset = Account.objects.filter(owner=request.user)
        table = AccountTable(queryset)
        table.paginate(page=request.GET.get('page', 1), per_page=10)
        if request.method == 'POST':
            form = AccountForm(request.POST)
            if form.is_valid():
                account = Account.objects.create(
                    owner=request.user,
                    exchange=form.cleaned_data['exchange'],
                    exchange_email=form.cleaned_data['exchange_email'],
                    exchange_password=form.cleaned_data['exchange_password'],
                    exchange_phone_number=form.cleaned_data['exchange_phone_number'],
                    token=form.cleaned_data['token'],
                    wallet_address=form.cleaned_data['wallet_address']
                )
                if account.token == '':
                    if account.exchange == str(ExchangeChoice.NOBITEX):
                        url = 'https://api.nobitex.ir/auth/login/'

                        payload = json.dumps({
                            'username': account.exchange_email,
                            'password': account.exchange_password,
                            "captcha": "api"
                        })
                        headers = {
                            "Content-Type": "application/json"
                        }

                        response = requests.request("POST", url, headers=headers, data=payload).json()
                        if 'status' in response and response['status'] == 'success':
                            account.token = response['key']
                            account.save()
                    elif account.exchange == str(ExchangeChoice.PHINIX):
                        url = "https://api.phinix.ir/auth/login"

                        payload = json.dumps({
                            "mobile_number": str(account.exchange_phone_number),
                            "password": account.exchange_password
                        })
                        headers = {
                            'Content-Type': 'application/json'
                        }

                        response = requests.request("POST", url, headers=headers, data=payload).json()
                        if 'status' in response and response['success']:
                            account.token = response['result']['token']
                            account.save()
        else:
            form = AccountForm()
        return render(request, 'exchange/account.html', {'form': form,
                                                         'table': table})


def account_edit_view(request, pk):
    account = Account.objects.get(pk=pk)
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account.token = form.cleaned_data['token']
            account.wallet_address = form.cleaned_data['wallet_address']
            account.save()
    else:
        form = AccountForm(initial={
            'exchange': account.exchange,
            'exchange_email': account.exchange_email,
            'exchange_phone_number': account.exchange_phone_number,
            'exchange_password': account.exchange_password
        })
    return render(request, 'exchange/edit_account.html', {'form': form})


def profitandloss_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    if request.method == 'POST':
        form = ProfitAndLossForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['ranged_show']:
                queryset = Transaction.objects.filter(customer=request.user,
                                                      dual_transaction__isnull=False,
                                                      status=Status.SUCCESS,
                                                      dual_transaction__status=Status.SUCCESS)
            else:
                queryset = Transaction.objects.filter(customer=request.user,
                                                      created__gte=form.cleaned_data['range_start'],
                                                      created__lte=form.cleaned_data['range_end'],
                                                      dual_transaction__isnull=False,
                                                      status=Status.SUCCESS,
                                                      dual_transaction__status=Status.SUCCESS)
            # queryset.annotate(profit_by_opposite=F('price')-F('dual_transaction__price'))
            table = TransactionTable(queryset)
            table.paginate(page=request.GET.get('page', 1), per_page=10)
            sell_side = queryset.filter(type=TransactionType.SELL).aggregate(sell_sum=Sum('price'),
                                                                             sell_fee=Sum('transaction-fee'))
            buy_side = queryset.filter(type=TransactionType.BUY).aggregate(buy_sum=Sum('price'),
                                                                           buy_fee=Sum('transaction_fee'))
            sell_sum, sell_fee = sell_side['sell_sum'], sell_side['sell_fee']
            buy_sum, buy_fee = buy_side['buy_sum'], buy_side['buy_fee']

            if not sell_sum:
                sell_sum = 0
            if not buy_sum:
                buy_sum = 0
            if not sell_fee:
                sell_fee = 0
            if not buy_fee:
                buy_fee = 0
            final = sell_sum - buy_sum - sell_fee - buy_fee
            return render(request, 'exchange/profitandloss.html', {'form': form,
                                                                   'table': table,
                                                                   'final': final})
    else:
        form = ProfitAndLossForm()
        table = TransactionTable(Transaction.objects.filter(customer=request.user))
        return render(request, 'exchange/profitandloss.html', {'form': form,
                                                               'table': table,
                                                               'final': 'Please specify range to Calculate Profit and Loss'})


def orderbooks_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    if request.method == 'POST':
        form = ChoiceExchangeForm(request.POST)
        if form.is_valid():
            coin = form.cleaned_data['currency']
            bids = cache.get(str(coin).upper() + "bids")
            asks = cache.get(str(coin).upper() + "asks")
            bids_table = BidsTable(bids)
            asks_table = AsksTable(asks)
            return render(request, 'exchange/orderbooks.html', {'form': form,
                                                                'bids_table': bids_table,
                                                                'asks_table': asks_table, })
    else:
        form = ChoiceExchangeForm()
        return render(request, 'exchange/orderbooks.html', {'form': form})


def trade_view(request, currency, market):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    asks = cache.get(currency + str(market).lower() + 'ask')
    bids = cache.get(currency + str(market).lower() + 'bid')
    bids_table = BidsTable(bids)
    asks_table = AsksTable(asks)
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            exchange = form.cleaned_data['exchange']
            crypto = form.cleaned_data['crypto']
            size = form.cleaned_data['size']
            price = form.cleaned_data['price']
            trade_type = form.cleaned_data['type']
            transaction_id, status, message = None, None, None

            account = Account.objects.get(owner=request.user, exchange=exchange)
            if exchange == str(ExchangeChoice.NOBITEX):
                url = "https://api.nobitex.ir/market/orders/add"
                payload = json.dumps({
                    "type": str(trade_type).lower(),
                    "srcCurrency": str(crypto).lower(),
                    "dstCurrency": 'usdt',
                    'amount': str(size),
                    "price": price
                })
                headers = {
                    "Authorization": "Token " + account.token,
                    "content-type": "application/json"
                }

                response = requests.request("POST", url, headers=headers, data=payload).json()
                status = response['status']
                message = "The operation was successful"
                if status == 'failed':
                    message = response['message']
                else:
                    transaction_id = response['order']['id']
                print(response)
            else:
                url = 'https://api.' + exchange.lower() + '.ir/v1/account/orders'
                payload = json.dumps({
                    "price": str(price),
                    "quantity": str(size),
                    "side": trade_type.lower(),
                    "symbol": crypto + "USDT",
                    "type": "market"
                })
                headers = {
                    'Authorization': 'Bearer ' + account.token,
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload).json()
                status = response['success']
                message = response['message']
                if status:
                    transaction_id = response['result']['clientOrderId']
            if status is True or status == 'ok':
                transaction = Transaction.objects.create(customer=request.user,
                                                         crypto=crypto,
                                                         exchange=exchange,
                                                         status=Status.PENDING,
                                                         type=trade_type,
                                                         size=size,
                                                         price=price,
                                                         transaction_id=transaction_id)
                if trade_type is TransactionType.BUY:
                    dual = Transaction.objects.filter(type=TransactionType.SELL,
                                                      customer=request.user, crypto=crypto). \
                        order_by('-created')[0]
                    dual.dual_transaction = transaction
                    transaction.dual_transaction = dual
            return render(request, 'exchange/trade.html', {'form': form,
                                                           'status': status,
                                                           'message': message,
                                                           'asks': asks_table,
                                                           'bids': bids_table})
    else:
        form = TradeForm(initial={
            'crypto': currency,
            'exchange': str(market).capitalize()
        })
        return render(request, 'exchange/trade.html', {'form': form,
                                                       'status': '',
                                                       'message': '',
                                                       'asks': asks_table,
                                                       'bids': bids_table})


def choice_details(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            exchange = form.cleaned_data['exchange']
            crypto = form.cleaned_data['crypto']
            return redirect('/exchange/trade/' + crypto + '/' + str(exchange).lower())

    else:
        form = ChoiceForm()
        return render(request, 'exchange/choice.html', {'form': form})


def withdraw_view(request):
    if not request.user.is_authenticated:
        return HttpResponse('Please login first...')
    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            exchange = form.cleaned_data['exchange']
            currency = form.cleaned_data['currency']
            wallet_address = form.cleaned_data['wallet_address']
            wallet_id = form.cleaned_data['wallet_id']
            network = form.cleaned_data['network']
            amount = form.cleaned_data['amount']
            totp = form.cleaned_data['one_time_password']

            account = Account.objects.get(exchange=ExchangeChoice.NOBITEX, owner=request.user)
            if exchange == str(ExchangeChoice.NOBITEX):
                url = 'https://api.nobitex.ir/users/wallets/withdraw'

                payload = json.dumps({
                    'wallet': wallet_id,
                    'network': network,
                    'amount': amount,
                    'address': wallet_address
                })
                headers = {
                    'Content-Type': 'application/json',
                    "Authorization": "Token " + account.token,
                    'X-TOTP': totp
                }

                response = requests.request('POST', url, headers=headers, data=payload).json()
                print(response)
                if 'status' in response and response['status'] == 'ok':
                    redirect('/withdraw-confirm/' + response['withdraw']['id'])
                else:
                    status = response['message']
                    return render(request, 'exchange/withdraw.html', {'form': form,
                                                                      'status': status})
            else:
                return HttpResponse('No Withdraw API provided for other Exchanges :((')
    else:
        form = WithdrawForm()
        return render(request, 'exchange/withdraw.html', {'form': form,
                                                          'status': ""})


def withdraw_confirm_view(request, withdraw_id):
    if not request.user.is_authenticated:
        return HttpResponse("Please login first...")
    if request.method == "POST":
        form = WithdrawConfirmForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['one_time_password']

            account = Account.objects.get(exchange=ExchangeChoice.NOBITEX, owner=request.user)
            url = 'https://api.nobitex.ir/users/wallets/withdraw-confirm'
            payload = json.dumps({
                'withdraw': withdraw_id,
                'otp': otp
            })
            headers = {
                'Content-Type': 'application/json',
                "Authorization": "Token " + account.token,
            }

            response = requests.request('POST', url, headers=headers, data=payload).json()

            if 'status' in response and response['status'] == 'ok':
                status = "Withdraw done successfully"
            else:
                status = response['message']
            return render(request, 'exchange/withdraw-confirm.html', {'form': form,
                                                                      'status': status})
    else:
        form = WithdrawConfirmForm()
        return render(request, 'exchange/withdraw-confirm.html', {'form': form,
                                                                  'status': ''})

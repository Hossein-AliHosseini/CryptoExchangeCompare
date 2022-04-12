from django.shortcuts import render
from django.http import HttpResponse

from .tables import TransactionTable, AccountTable
from .models import Transaction, Account
from .forms import AccountForm


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
                    user=request.user,
                    exchange=form.cleaned_data['exchange'],
                    exchange_email=form.cleaned_data['exchange_email'],
                    exchange_password=form.cleaned_data['exchange_password'],
                    exchange_phone_number=form.cleaned_data['exchange_phone_number']
                )
        else:
            form = AccountForm()
        return render(request, 'exchange/account.html', {'form': form,
                                                         'table': table})

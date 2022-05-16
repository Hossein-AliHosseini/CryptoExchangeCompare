from django.db import models


class ReportType:
    ACCOUNTS = 'Accounts',
    TRANSACTIONS = 'Transactions'

    TYPES = (
        (ACCOUNTS, 'Accounts'),
        (TRANSACTIONS, 'Transactions')
    )

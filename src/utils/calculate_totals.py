# src/utils/calculate_totals.py
from datetime import datetime
from decimal import Decimal


def calculate_totals(transactions):
    total_all_sales = Decimal("0")
    total_this_month = Decimal("0")
    total_today = Decimal("0")

    today = datetime.today().date()
    start_of_month = today.replace(day=1)

    for transaction in transactions:
        total_all_sales += transaction.total

        if transaction.date >= start_of_month:
            total_this_month += transaction.total

        if transaction.date == today:
            total_today += transaction.total

    return total_all_sales, total_this_month, total_today

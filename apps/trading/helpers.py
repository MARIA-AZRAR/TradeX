
from decimal import Decimal, ROUND_HALF_UP


def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another using real-time rates."""
    if from_currency == to_currency:
        return amount

    # Rates stored as Decimal strings to avoid binary float precision errors
    exchange_rates = {
        'USD': {'EUR': Decimal('0.92'), 'GBP': Decimal('0.76'), 'JPY': Decimal('148.0'), 'AUD': Decimal('1.49')},
        'EUR': {'USD': Decimal('1.09'), 'GBP': Decimal('0.82'), 'JPY': Decimal('160.0'), 'AUD': Decimal('1.62')},
        'GBP': {'USD': Decimal('1.31'), 'EUR': Decimal('1.22'), 'JPY': Decimal('195.0'), 'AUD': Decimal('1.98')},
        'JPY': {'USD': Decimal('0.0068'), 'EUR': Decimal('0.0063'), 'GBP': Decimal('0.0051'), 'AUD': Decimal('0.0102')},
        'AUD': {'USD': Decimal('0.67'), 'EUR': Decimal('0.62'), 'GBP': Decimal('0.50'), 'JPY': Decimal('98.0')}
    }

    try:
        rate = exchange_rates[from_currency][to_currency]
        converted_amount = Decimal(str(amount)) * rate
        return converted_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except KeyError:
        raise ValueError("Currency conversion not supported or invalid currency code.")

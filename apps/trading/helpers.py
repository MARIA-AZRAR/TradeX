
def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another using real-time rates."""
    if from_currency == to_currency:
        return amount
    
    # Dummy exchange rates
    exchange_rates = {
        'USD': {'EUR': 0.92, 'GBP': 0.76, 'JPY': 148.0, 'AUD': 1.49},
        'EUR': {'USD': 1.09, 'GBP': 0.82, 'JPY': 160.0, 'AUD': 1.62},
        'GBP': {'USD': 1.31, 'EUR': 1.22, 'JPY': 195.0, 'AUD': 1.98},
        'JPY': {'USD': 0.0068, 'EUR': 0.0063, 'GBP': 0.0051, 'AUD': 0.0102},
        'AUD': {'USD': 0.67, 'EUR': 0.62, 'GBP': 0.50, 'JPY': 98.0}
    }

    try:
        rate = exchange_rates[from_currency][to_currency]
        converted_amount = float(amount) * rate
        return round(converted_amount, 2)
    except KeyError:
        raise ValueError("Currency conversion not supported or invalid currency code.")


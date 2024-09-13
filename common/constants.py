
CURRENCY_CHOICES = [
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
    ('JPY', 'Japanese Yen'),
    ('AUD', 'Australian Dollar')
]


class ErrorMessages:
    INVALID_SHARES_VALUE = "Volume should be less than or Equal to Outstanding Shares"
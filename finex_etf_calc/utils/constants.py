class CurrenciesNames:
    RUB = 'RUB'
    EUR = 'EUR'
    KZT = 'KZT'
    USD = 'USD'

    @classmethod
    def get_attributes(cls):
        return [attr for attr in dir(cls) if not attr.startswith('_')]

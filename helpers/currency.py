import requests


class CurrencyConverter:
    """
    A singleton currency converter object with a base currency.

    args:
        base (str): to which currency to convert
    """
    _instance = None

    def __new__(cls, base: str):
        """ Define a singleton class. """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, base: str):
        """ Initiate the object and get the conversion rates. """
        url = f'https://api.exchangerate-api.com/v4/latest/{base}'
        self.base = base
        self.rates = requests.get(url).json().get('rates')

    def calc(self, value: float, current: str) -> float:
        """
        Convert a value on current currency to the base currency.

        args:
            value (float): money value to convert
            current (str): in which currency is the value

        returns:
            (float): converted amount in base currency
        """
        return value / self.rates.get(current.upper())


if __name__ == '__main__':
    cc1 = CurrencyConverter('brl')
    cc2 = CurrencyConverter('brl')
    print(f'cc1 == cc2? {cc1 == cc2}')
    print(f'cc1.__hash__(): {cc1.__hash__()}')
    print(f'cc2.__hash__(): {cc2.__hash__()}')
    print(cc1.rates)
    print(cc1.calc(1, 'usd'))

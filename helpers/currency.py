import requests


class CurrencyConverter():
    def __init__(self, base: str):
        """
        Define a currency converter object with a base currency.

        args:
            base (str): to which currency to convert
        """
        url = f'https://api.exchangerate-api.com/v4/latest/{base}'
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
        return value / self.rates.get(current)


if __name__ == '__main__':
    cc = CurrencyConverter('BRL')
    print(cc.rates)
    print(cc.calc(1, 'USD'))

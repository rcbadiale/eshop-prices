from time import time

from config import CURRENCY, DB_PATH, STORES_CURRENCY, STORES_GET, TAX
from helpers import CurrencyConverter, data_to_html, simple_mail
from modules import DB, Game, get_price_store, Search


def convert_currencies(cc: CurrencyConverter, game: Game):
    """
    Convert the prices dictionary from the Game object to the desired currency.

    args:
        cc: CurrencyConverter object with base currency
        game: Game object which the prices will be converted to base currency
    """
    game.prices = {
        store: cc.calc(value, STORES_CURRENCY.get(store))
        if value else None for store, value in game.prices.items()
    }


def multiply_iof(game: Game, ignored_stores: list = ['BR']):
    """
    Add taxes to the converted prices.

    args:
        game: Game object which the taxes will be added
        ignored_stores (list): stores to be ignored
    """
    for store, price in game.prices.items():
        if store in ignored_stores:
            game.prices[store] = round(price * TAX, 2) if price else None


def main():
    """
    Main code to be ran.
    """
    cc = CurrencyConverter(CURRENCY)
    db = DB(DB_PATH)
    search = Search()

    print('Searching all games...')
    search.all_games()
    games = [Game(**each) for each in search.games_list]
    for store in STORES_GET:
        print(f'Getting prices from {store} store...')
        get_price_store(games, store)

    to_add = []
    print('Converting prices and adding taxes...')
    for game in games:
        convert_currencies(cc, game)
        multiply_iof(game)
        to_add.append(game.__dict__)

    print('Saving to DB...')
    db.insert_multiple(to_add)
    print('Saved!')

    diff = [
        x['nid'] for x in db.find('sale', True)
        if not db.clone.search(
            db._query.fragment({'nid': x['nid'], 'discount': x['discount']})
        )
    ]
    to_send = [game for game in games if game.nid in diff]

    if len(to_send) > 0:
        print('Sending email...')
        mail_content = data_to_html(to_send)
        simple_mail('Switch games on sale', mail_content)
        print('Email sent!')


if __name__ == '__main__':
    """
    Start main function and do some simple time monitoring.
    """
    start = time()
    main()
    runtime = time() - start
    hours = runtime // 3600
    minutes = runtime // 60 - (hours * 60)
    seconds = runtime - (minutes * 60)
    print(f'Runtime: {hours:.0f}h {minutes:.0f}m {seconds:.0f}s')

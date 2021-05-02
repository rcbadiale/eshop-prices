from helpers.template import card_template, content_template, html_template

TAX_NAME = 'IOF'
PRICE_UNIT = 'R$'


def data_to_html(games: list, store: str):
    """
    Convert games data into a HTML Table for the email.

    args:
        games (list): List of Game Objects with prices and discounts
        store (str): Base store
    """
    should_return = False
    cards = ''
    for game in games:
        if game.sale:
            should_return = True

            content = ''
            for key, price in game.prices.items():
                content += content_template.format(
                    store=(
                        key.upper() if key.lower() == store.lower()
                        else f'{key.upper()} + {TAX_NAME}'
                    ),
                    unit=PRICE_UNIT,
                    price=price
                )

            cards += card_template.format(
                img=game.img, url=game.url, title=game.title,
                content=content, discount=game.discount
            )

    return html_template.format(
        qty=len(games), cards=cards
    ) if should_return else None

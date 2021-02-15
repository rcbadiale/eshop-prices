# Table styling
A = (
    'color: black;'
    'font-weight: bold;'
)
TABLE = 'border-collapse: collapse;'
TR = (
    'border-collapse: collapse;'
    'border: 1px solid black;'
)
TD = (
    'border-right: 1px solid black;'
    'min-width: 2.5rem;'
    'padding: 0 10px;'
)
TDCENTER = f'{TD}text-align: center;'
TH = (
    'border-right: 1px solid black;'
    'min-width: 2.5rem;'
    'padding: 0 10px;'
)


def data_to_html(games: list):
    """
    Convert games data into a HTML Table for the email.

    args:
        games (list): List of Game Objects with prices and discounts
    """
    should_return = False
    headers = ['Title', 'US + IOF', 'BR', 'Discount (%)']
    text = (
        f'Switch games on sale:<br><br>'
        f'<br><table style="{TABLE}"><thead>'
        f'<tr style="{TR}">'
    )
    for ind in headers:
        text += f'<th style="{TH}">{ind}</th>'
    text += '</tr></thead><tbody>'
    for game in games:
        if game.sale:
            should_return = True
            price_us = (
                f'R$ {game.prices.get("US"):.2f}'
                if game.prices.get("US") else '-'
            )
            price_br = (
                f'R$ {game.prices.get("BR"):.2f}'
                if game.prices.get("BR") else '-'
            )
            text += (
                f'<tr style="{TR}">'
                f'<td style="{TD}">'
                f'<a style="{A}" href="{game.url}">{game.title}</a>'
                f'</td>'
                f'<td style="{TDCENTER}">{price_us}</td>'
                f'<td style="{TDCENTER}">{price_br}</td>'
                f'<td style="{TDCENTER}">{game.discount}</td>'
                '</tr>'
            )
    text += '</body></html>'
    return text if should_return else None

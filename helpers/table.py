from helpers.template import card_template, html_template


def data_to_html(games: list):
    """
    Convert games data into a HTML Table for the email.

    args:
        games (list): List of Game Objects with prices and discounts
    """
    should_return = False
    cards = ''
    for game in games:
        if game.sale:
            should_return = True

            headers_list = [
                key.upper() if key == 'BR'
                else f'{key.upper()} + IOF'
                for key in game.prices.keys()
            ]
            headers_list.append('Discount')

            headers = ''
            for ind in headers_list:
                headers += f'<th>{ind}</th>'

            values = ''
            for price in game.prices.values():
                values += f'<td>{price:.2f}</td>'
            values += f'<td>{game.discount:d}%</td>'

            cards += card_template.format(
                img=game.img, length=len(headers_list), url=game.url,
                title=game.title, headers=headers, values=values
            )

    return html_template.format(
        qty=len(games), cards=cards
    ) if should_return else None

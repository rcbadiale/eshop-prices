import requests

API_URL = 'https://api.ec.nintendo.com/v1/price?lang=en&'


def call_eshop_api(multiple_nids: str, country: str):
    """
    Send eShop API requests for multiple Nintendo IDs.

    args:
        multiple_nids (str): multiple nIDs as comma separated string
        country (str): define the store country for the API
    """
    url = f'{API_URL}country={country}&ids={multiple_nids}'
    data = requests.get(url).json().get('prices')

    price_nid = {}
    for item in data:
        nid = str(item['title_id'])
        if item.get('sales_status') == 'onsale':
            sale_price = item.get('discount_price', {}).get('raw_value')
            full_price = item.get('regular_price', {}).get('raw_value')
            sale = True if sale_price else False
            discount = round((
                1 - float(sale_price) / float(full_price)
            ) * 100) if sale else 0

            price_nid[nid] = {
                'sale': sale,
                'discount': discount,
                'prices': {
                    country: (
                        float(sale_price) if sale_price
                        else float(full_price)
                    )
                },
            }
    return price_nid


def get_price_store(games: list, country: str):
    """
    Use Nintendo eShop API to get prices from specified country.

    This method will write the prices, discount and sale properties.

    args:
        games (list): list of Game objects
        country (str): define the store country for the API
    """
    all_nids = [game.nid for game in games]
    nids_list = [
        ','.join(all_nids[i:i + 50]) for i in range(0, len(all_nids), 50)
    ]

    price_nid = {}
    for nids_as_str in nids_list:
        price_nid.update(call_eshop_api(nids_as_str, country.upper()))

    for game in games:
        if price_nid.get(game.nid):
            tmp = price_nid.get(game.nid)
            game.sale = game.sale or tmp.get('sale')
            game.discount = max(game.discount, tmp.get('discount'))
            game.prices.update(tmp.get('prices'))

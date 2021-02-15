from algoliasearch.search_client import SearchClient

# Nintendo data from Nintendo Game Store
APP_ID = "U3B6GR4UA3"
API_KEY = "c4da8be7fd29f0f5bfa42920b0a99dc7"
INDEX_NAME = "ncom_game_en_us"
NINTENDO_URL = 'https://www.nintendo.com'


class Search():
    """
    Algolia Search object to get full list of games for the Switch.
    """
    def __init__(self):
        self.games_list = []
        self.client = SearchClient.create(APP_ID, API_KEY)
        self.index = self.client.init_index(INDEX_NAME)

    def all_games(self):
        """
        Run through multiple queries to get a full list of games available.

        This method will run through the queries until there is 5 empty
        queries.

        The results will be added to the property 'games_list' as a dict for
        each game found.
        """
        self.query_empty = 0
        self.query_sequence = 0

        while self.query_empty < 5:
            query = f'7001{self.query_sequence:08}'
            response = self.index.search(query).get('hits', [])
            self.query_sequence += 1

            if len(response) > 0:
                self.query_empty = 0
                for each in response:
                    art = each.get('boxart', None)
                    price = each.get('lowestPrice')
                    sale = True if each.get('salePrice') else False
                    discount = round((
                        1 - float(price) / float(each.get('msrp'))
                    ) * 100) if sale else 0

                    self.games_list.append({
                        'nid': each['nsuid'],
                        'title': each['title'],
                        'desc': each['description'],
                        'url': f"{NINTENDO_URL}{each['url']}",
                        'img': f"{NINTENDO_URL}{art}" if art else None,
                        'sale': sale,
                        'discount': discount,
                        'prices': {
                            'US': float(price) if price else None
                        },
                    })
            else:
                self.query_empty += 1

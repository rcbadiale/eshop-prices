from typing import Any

from tinydb import Query, TinyDB


class DB():
    def __init__(
        self,
        path: str,
        table_name: str = 'games_list',
        backup_table='backup'
    ):
        """
        TinyDB object where the games information will be saved for future use.

        args:
            path (str): local path for the DB file (.json)
            table_name (str): table which will receive the information
            backup_table (str): table to backup the previous information
        """
        self._db = TinyDB(path)
        self._table_name = table_name
        self.table = self._db.table(self._table_name)
        self._query = Query()
        self.clone_table(backup_table)

    def insert(self, data: dict):
        """
        Insert/Update data into the DB

        args:
            data (dict): data to be added, if the Title already
                exists it will be updated.
        """
        self.table.upsert(data, self._query.title == data.get('title'))

    def find(self, key: str, item: Any):
        """
        Find data from the DB

        args:
            key (str): key to search
            item (Any): wished data to be found on key
        """
        return self.table.search(self._query[key] == item)

    def get_all_ids(self):
        """
        Get all Nintendo IDs from DB.
        """
        return [each['nid'] for each in self.table.all()]

    def drop_table(self, table_name: str):
        """
        Delete a table from the DB.

        args:
            table_name (str): table which will be deleted
        """
        self._db.drop_table(table_name)

    def update_game(self, game_title: str, data: dict):
        """
        Update game data for the given title.

        args:
            game_title (str): game title to be changed
            data (dict): data to be updated/added
        """
        self.table.update(data, self._query['title'] == game_title)

    def clone_table(self, clone_name: str):
        """
        Clone original table to the desired one.

        args:
            clone_name (str): name of the new table
        """
        self.drop_table(clone_name)
        self.clone = self._db.table(clone_name)
        self.clone.insert_multiple(self.table.all())


if __name__ == '__main__':
    """
    A bunch of tests to see the DB Object working.
    """
    db = DB('db.json', 'test')
    print('Inserting 2 games...')
    db.insert({
        'title': 'This is only a game',
        'desc': 'ABC TEST DEF.',
        'nid': '1234',
        'url': 'http://xpto.com',
        'img': 'http://xpto.com/png.png',
        'full_price': 300,
        'price': 250,
        'sale': True,
        'discount': 16.67,
    })
    db.insert({
        'title': 'This is only a game 2',
        'desc': 'ABC TEST DEF TEST GHI.',
        'nid': '1235',
        'url': 'http://xpto.com',
        'img': 'http://xpto.com/png2.png',
        'full_price': 300,
        'price': 300,
        'sale': False,
        'discount': '-',
    })

    print('Show first game info:')
    print(db.find('title', 'This is only a game'))

    print('Updated first game info:')
    db.update_game('This is only a game', {'price': 200, 'discount': 33.33})
    print(db.find('title', 'This is only a game'))

    print('Show second game info:')
    print(db.find('title', 'This is only a game 2'))

    print('Insert second game info with updated data:')
    db.insert({
        'title': 'This is only a game 2',
        'desc': 'ABC TEST DEF TEST GHI.',
        'nid': '1235',
        'url': 'http://xpto.com',
        'img': 'http://xpto.com/png2.png',
        'full_price': 300,
        'price': 250,
        'sale': True,
        'discount': 16.67,
    })
    print(db.find('title', 'This is only a game 2'))

    print('Drop test table')
    db.drop_table()

    print('EOF')

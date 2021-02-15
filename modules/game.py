class Game:
    def __init__(self, nid: str, title: str, **kwargs):
        """
        Nintendo Switch game object with basic game information.

        args:
            nid (str): Nintendo game ID
            title (str): game title
        common kwargs:
            desc (str): game description
            url (str): game URL
            img (str): game image URL
            sale (bool): True if game is on sale
            discount (float): discount value
            prices (dict): game prices in the formate {'STORE': 'PRICE'}
        """
        self.nid = nid
        self.title = title
        self.sale = False
        self.discount = 0
        self.prices = {}
        self.__dict__.update(kwargs)

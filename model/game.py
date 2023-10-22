class Game:
    def __init__(self, title, description, original_price, img, from_date, to_date):
        self._title = title
        self._description = description
        self._original_price = original_price
        self._img = img
        self._from_date = from_date
        self._to_date = to_date

    def __str__(self):
        return f"('title': {self._title}, " \
               f"'description': {self._description}, " \
               f"'original_price': {self._original_price}, " \
               f"'img': {self._img}, " \
               f"'from_date': {self._from_date}, " \
               f"'to_date': {self._to_date},)"

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_original_price(self):
        return self._original_price

    def get_img(self):
        return self._img

    def get_from_date(self):
        return self._from_date

    def get_to_date(self):
        return self._to_date

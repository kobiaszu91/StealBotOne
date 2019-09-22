"""my docstring"""

from datetime import datetime


class Offer:
    """my docstring"""
    def __init__(self, title, link, link_image, new_price, old_price, color=''):
        self._title = title
        self._url = link
        self._url_image = link_image
        self._date = datetime.now()
        self._new_price = new_price
        self._old_price = old_price
        self._color = color


    def get_insert_offer_query(self):
        """my docstring"""
        return "INSERT INTO offers VALUES " + "('" + self._title + "', '" + \
               self._url + "', '" + self._url_image + "', '" \
               + self._date.strftime("%m/%d/%Y, %H:%M:%S") + \
               "', '" + str(self._new_price) + "', '" + str(self._old_price) + "', '" + \
               self._color + "')"

    def get_remove_offer_query(self):
        """my docstring"""
        return "DELETE FROM offers WHERE title=? AND color=?", (self._title, self._color)

    def print_offer(self):
        """my docstring"""
        print(self._title + ' ' + self._color + ' ' + self._url + ' ' + str(self._date) +
              ' old price: ' + \
              str(self._old_price) + ' new price: ' + str(self._new_price))

    def get_bot_message(self):
        """my docstring"""
        return self._title + ' ' + self._color + ' ' + self._url + ' ' + ' old price: ' + \
              str(self._old_price) + ' new price: ' + str(self._new_price)

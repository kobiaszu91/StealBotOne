
from offer import Offer
from NikeScrapper import NikeScrapper
from AdidasScrapper import AdidasScrapper
from AboutYou_scrapper import AboutYou_scrapper

import time

TeleBot_ID = 390569459

class UpdateSteals:
    def __init__(self, db_connection):
        self._db_connection = db_connection
        self._db_connection_cursor = self._db_connection.cursor()
        self._new_steals = []
        self._removed_steals = []

    def find_steals(self, bot):
        status = True
        self._db_connection_cursor.execute("SELECT * FROM offers")
        raw_db_steals = self._db_connection_cursor.fetchall()
        db_steals = []

        for db_steal in raw_db_steals:
            db_steal = (db_steal[: 3] + db_steal[3 + 1:])
            db_steal = Offer(db_steal[0], db_steal[1], db_steal[2], db_steal[3], db_steal[4], db_steal[5])
            # print(db_steal.print_offer())
            db_steals.append(db_steal)

        # aboutyou_scrapper = AboutYou_scrapper()
        # aboutyou_scrapper.find_steals()
        nikeScrapper = NikeScrapper()
        # adidasScrapper = AdidasScrapper()
        try:
            shop_steals = nikeScrapper.find_steals()
        except:
            bot.sendMessage(TeleBot_ID, "Problem with connecting to Nike.com, cooldown for 5 minuites")
            time.sleep(300)
            return False
        # shop_steals = adidasScrapper.find_steals()

        exists = 0
        self._new_steals = []
        for new_steal in shop_steals:
            for db_steal in db_steals:
                if new_steal._title == db_steal._title and new_steal._color == db_steal._color:
                    exists = 1
            if not exists:
                self._new_steals.append(new_steal)
                self._db_connection_cursor.execute(new_steal.get_insert_offer_query())
                db_steals.append(new_steal)
            exists = 0
        self._db_connection.commit()

        exists = 0
        self._removed_steals = []
        for db_steal in db_steals:
            for new_steal in shop_steals:
                if new_steal._title == db_steal._title and new_steal._color == db_steal._color:
                    exists = 1
            if not exists:
                self._removed_steals.append(db_steal)
                self._db_connection_cursor.execute("DELETE FROM offers WHERE title=? AND color=?", (db_steal._title, db_steal._color))
            exists = 0
        self._db_connection.commit()
        return status

    def get_db_steals(self):
        return self._db_connection_cursor.fetchall(self._db_connection_cursor.execute("SELECT * FROM offers"))

    def get_new_steals(self):
        return self._new_steals

    def get_removed_steals(self):
        return self._removed_steals

    def print_db_steals(self):
        for db_steal in self._db_connection_cursor.fetchall(self._db_connection_cursor.execute("SELECT * FROM offers")):
            db_steal.print_offer()

    def print_new_steals(self):
        for new_steal in self._new_steals:
            new_steal.print_offer()

    def print_removed_steals(self):
        for removed_steal in self._removed_steals:
            removed_steal.print_offer()

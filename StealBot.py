import telepot
import sqlite3
from UpdateSteals import UpdateSteals
import time

conn = sqlite3.connect('offer.db')
c = conn.cursor()
#fff

# c.execute("""CREATE TABLE offers (
#          title text,
#          url text,
#          url_image text,
#          date text,
#          new price integer,
#          old price integer,
#          color text)""")

conn.commit()


TeleBot_ID = 390569459
bot = telepot.Bot('603684646:AAFhSxb6tbmh8F4QkDjMyi1fl9U9pluPFhc')
bot.setWebhook()


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print('Got command: %s' + command)
    bot.sendMessage(chat_id, command)


def main():
    updateSteals = UpdateSteals(conn)
    bot.sendMessage(TeleBot_ID , "StealBot active!")

    while 1:
        updateSteals.find_steals()
        print("NEW AVAILABLE STEALS: ")
        updateSteals.print_new_steals()
        for new_steal in updateSteals.get_new_steals():
            bot.sendMessage(TeleBot_ID, new_steal.get_bot_message())
        print("REMOVED STEALS STEALS: ")
        updateSteals.print_removed_steals()
        for removed_steal in updateSteals.get_removed_steals():
            bot.sendMessage(TeleBot_ID, removed_steal.get_bot_message())
        time.sleep(180)


if __name__ == "__main__":
    main()















import telepot
import sqlite3
from UpdateSteals import UpdateSteals
import time
from StealBot_Status import Steal_Status

conn = sqlite3.connect('offer.db')
c = conn.cursor()


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
bot_status = Steal_Status.STOPPED


def handle(msg):
    global bot_status
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, "You said '{}'".format(msg["text"]))
    if content_type == 'text':
        message = msg["text"].lower()
        if "stop" in message:
            bot_status = Steal_Status.STOPPED
            bot.sendMessage(TeleBot_ID, "Telepot: Stopping StealBot!")
        if "start" in message:
            bot_status = Steal_Status.RUNNING
            bot.sendMessage(TeleBot_ID, "Telepot: Resuming StealBot!")


bot.message_loop(handle)

def main():
    updateSteals = UpdateSteals(conn)
    bot.sendMessage(TeleBot_ID, "StealBot active!")
    while 1:
        if bot_status == Steal_Status.RUNNING:
            bot.sendMessage(TeleBot_ID,"StealBot: SCANNING!")
            if not updateSteals.find_steals(bot):
                continue
            bot.sendMessage(TeleBot_ID, "StealBot: SCAN FINNISHED!")
            bot.sendMessage(TeleBot_ID, "StealBot: NEW AVAILABLE STEALS:")
            updateSteals.print_new_steals()
            for new_steal in updateSteals.get_new_steals():
                bot.sendMessage(TeleBot_ID, new_steal.get_bot_message())
            bot.sendMessage(TeleBot_ID, "StealBot: REMOVED STEALS STEALS:")
            updateSteals.print_removed_steals()
            for removed_steal in updateSteals.get_removed_steals():
                bot.sendMessage(TeleBot_ID, removed_steal.get_bot_message())
            for i in range(300):
                i += 1
                time.sleep(1)
                if bot_status == Steal_Status.STOPPED:
                    break
        else:
            bot.sendMessage(TeleBot_ID, "StealBot: paused!")
            while bot_status == Steal_Status.STOPPED:
                time.sleep(1)
            bot.sendMessage(TeleBot_ID, "StealBot: resumed!!")




if __name__ == "__main__":
    main()

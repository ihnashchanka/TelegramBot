import config
import telebot
from random import shuffle
from Game import Game
import utils
from PostgreSQL import PostgreSQL


bot = telebot.TeleBot(config.token)
bot.set_webhook(url='https://fathomless-thicket-27571.herokuapp.com/');

@bot.message_handler(commands=['game'])
def play(message):
    new_game = Game(message.from_user.id)
    bot.send_message(message.chat.id, 'User ' + message.from_user.first_name + ' has started the game')
    bot.send_voice(message.chat.id, new_game.get_song())
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,selective=True)
    options = new_game.get_answers()
    shuffle(options)
    for item in options:
        markup.row(item)
    bot.reply_to(message, text=message.from_user.first_name + " please, choose the option",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def answer_to_all(message):
    if utils.is_in_game(message.from_user.id):
        cur_game = Game(message.from_user.id)
        if message.text == cur_game.get_right_answer():
            bot.send_message(message.chat.id, text=message.from_user.first_name + ", you are right!!!")
            #some other way to hide keyboard
            #bot.reply_to(message, text=message.from_user.first_name + ", you are right!!!",
                   #      reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
        else:
            bot.send_message(message.chat.id, text=message.from_user.first_name + ",sorry, you are wrong(((")
           #bot.reply_to(message, text=message.from_user.first_name + ",sorry, you are wrong(((",
                   #      reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
        cur_game.finish()
    else:
        bot.send_message(message.chat.id, "hi")

'''
@bot.message_handler(func=lambda message: True, content_types=['text'])
def answer_to_all(message):
    db = PostgreSQL(config.database_name)
    item = db.select_all('users')
    bot.send_message(message.chat.id, item[:])
'''
if __name__ == '__main__':
    state = "ckeck"
    bot.polling(none_stop=True)

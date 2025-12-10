from loader import bot
from telebot.types import Message

@bot.message_handler(commands=['start'])
def start_message_handler(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Бот работает')
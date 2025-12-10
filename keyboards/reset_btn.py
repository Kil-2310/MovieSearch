from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_remove_btn():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('🔄 Перезапустить бота'))
    return keyboard
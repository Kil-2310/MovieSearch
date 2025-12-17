from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_remove_btn():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('🔄 Перезапустить бота'))

    return keyboard


def get_amount_btn():
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("Первые 5", callback_data="first_5"),
        InlineKeyboardButton("Первые 10", callback_data="first_10"),
        InlineKeyboardButton("Первые 20", callback_data="first_20"),
        InlineKeyboardButton("Пропустить", callback_data="first_20")
    )

    return keyboard

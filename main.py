from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from database.bd_cinfig import create_models
import custom_handlers

if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    create_models()
    set_default_commands(bot)
    bot.infinity_polling()

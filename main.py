import os
import time
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# ======================== CONFIG ========================

# Token from environment variable or hardcoded
TOKEN = os.getenv("TOKEN", "8185936093:AAFeVtgngoz_fKo0a6LY-tYl8s4x6qlKFnU")

# Logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================== TEXTS ========================

WELCOME_MESSAGE = "🤖 Welcome to *PWizard Bot!*"
INFO_MESSAGE = (
    "✨ I can show you random fun facts, dog pics, motivational quotes, country details and more.\n\n"
    "🧰 Try these commands:\n"
    "• /catfact – Cat trivia 🐱\n"
    "• /dog – Cute dog photo 🐶\n"
    "• /bored – What to do? 🎲\n"
    "• /quote – Inspiring quote 💬\n"
    "• /poke – Pokémon profile 🎮\n"
    "• /country <name> – Country details 🌍\n"
    "• /user – Random profile 👤\n"
    "• /help – How this bot works 📚\n\n"
    "🔽 Use the menu below to explore."
)

HELP_TEXT = (
    "📚 *How to Use This Bot:*\n\n"
    "Here’s a list of things I can do:\n"
    "• /catfact – Fun cat trivia\n"
    "• /dog – Sends a dog photo\n"
    "• /bored – Suggests a random activity\n"
    "• /quote – Motivational quote\n"
    "• /poke – Shows Pokémon info\n"
    "• /country <name> – Country facts\n"
    "• /user – Generates a random profile\n\n"
    "You can also tap the buttons in the menu!"
)

# ======================== UTILS ========================

def send_typing_action(context: CallbackContext, chat_id: int):
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(1)

# ======================== COMMAND HANDLERS ========================

def start(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')
    time.sleep(1)
    send_typing_action(context, update.effective_chat.id)
    update.message.reply_text(INFO_MESSAGE, parse_mode='Markdown', reply_markup=main_menu())

def help_command(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    update.message.reply_text(HELP_TEXT, parse_mode='Markdown')

def cat_fact(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        response = requests.get("https://catfact.ninja/fact").json()
        update.message.reply_text(f"🐱 Cat Fact: {response['fact']}")
    except Exception as e:
        logger.error(e)
        update.message.reply_text("😿 Couldn't fetch cat fact.")

def dog_pic(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random").json()
        update.message.reply_photo(response['message'])
    except Exception as e:
        logger.error(e)
        update.message.reply_text("🐶 Couldn't fetch dog photo.")

def bored(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        response = requests.get("https://www.boredapi.com/api/activity").json()
        update.message.reply_text(f"🎲 Try this: {response['activity']}")
    except Exception as e:
        logger.error(e)
        update.message.reply_text("😞 Couldn't fetch an activity.")

def quote(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        response = requests.get("https://zenquotes.io/api/random").json()
        quote = response[0]['q']
        author = response[0]['a']
        update.message.reply_text(f"💬 {quote}\n— {author}", parse_mode='Markdown')
    except Exception as e:
        logger.error(e)
        update.message.reply_text("💬 Couldn't fetch quote.")

def poke(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu").json()
        name = response['name'].title()
        types = ', '.join([t['type']['name'] for t in response['types']])
        update.message.reply_text(f"🎮 Pokémon: {name}\nTypes: {types}", parse_mode='Markdown')
    except Exception as e:
        logger.error(e)
        update.message.reply_text("🎮 Couldn't fetch Pokémon info.")

def country(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        name = ' '.join(context.args)
        response = requests.get(f"https://restcountries.com/v3.1/name/{name}").json()[0]
        country_info = f"🌍 {response['name']['common']}\nCapital: {response['capital'][0]}\nRegion: {response['region']}\nPopulation: {response['population']}"
        update.message.reply_text(country_info, parse_mode='Markdown')
    except Exception as e:
        logger.error(e)
        update.message.reply_text("❌ Couldn’t find that country. Try another.")

def fake_user(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        response = requests.get("https://randomuser.me/api/").json()['data'][0]
        name = response['name']
        location = response['location']
        update.message.reply_text(
            f"👤 {name['first']} {name['last']}\n📧 {response['email']}\n🏙️ {location['city']}, {location['country']}",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(e)
        update.message.reply_text("👤 Couldn't fetch user profile.")

# ======================== MENU ========================

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🐱 Cat Fact", callback_data='catfact'), InlineKeyboardButton("🐶 Dog", callback_data='dog')],
        [InlineKeyboardButton("🎲 Bored", callback_data='bored'), InlineKeyboardButton("💬 Quote", callback_data='quote')],
        [InlineKeyboardButton("🎮 Pokémon", callback_data='poke'), InlineKeyboardButton("🌍 Country Info", callback_data='country')],
        [InlineKeyboardButton("👤 Fake User", callback_data='user')]
    ]
    return InlineKeyboardMarkup(keyboard)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    command_map = {
        'catfact': cat_fact,
        'dog': dog_pic,
        'bored': bored,
        'quote': quote,
        'poke': poke,
        'country': lambda u, c: u.callback_query.message.reply_text("🌍 Use /country <name> to get info."),
        'user': fake_user
    }

    if query.data in command_map:
        dummy_message = Update(update.update_id, message=query.message)
        command_map[query.data](update, context)

# ======================== MAIN ========================

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("catfact", cat_fact))
    dp.add_handler(CommandHandler("dog", dog_pic))
    dp.add_handler(CommandHandler("bored", bored))
    dp.add_handler(CommandHandler("quote", quote))
    dp.add_handler(CommandHandler("poke", poke))
    dp.add_handler(CommandHandler("country", country))
    dp.add_handler(CommandHandler("user", fake_user))
    dp.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot started.")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

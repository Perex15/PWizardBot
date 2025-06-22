# PWizard Bot: Fully cleaned, styled, animated, debugged for Python 3.11.0
# Includes inline menu, bottom menu, /ping command, and webhook-ready setup

import os
import time
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# ======================== CONFIG ========================
TOKEN = os.getenv("TOKEN", "8185936093:AAFeVtgngoz_fKo0a6LY-tYl8s4x6qlKFnU")
PORT = int(os.environ.get('PORT', '8442'))

# Enable logging to file and console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================== TEXTS ========================
WELCOME_MESSAGE = "\U0001F916 Welcome to *PWizard Bot!*"
INFO_MESSAGE = (
    "\u2728 I can show you random fun facts, dog pics, motivational quotes, country details and more.\n\n"
    "\U0001F9F0 Try these commands:\n"
    "• /catfact – Cat trivia \U0001F431\n"
    "• /dog – Cute dog photo \U0001F436\n"
    "• /bored – What to do? \U0001F3B2\n"
    "• /quote – Inspiring quote \U0001F4AC\n"
    "• /poke – Pokémon profile \U0001F3AE\n"
    "• /country <name> – Country details \U0001F30D\n"
    "• /user – Random profile \U0001F464\n"
    "• /ping – Check bot speed \U0001F4E1\n"
    "• /help – How this bot works \U0001F4DA"
)
HELP_TEXT = INFO_MESSAGE

# ======================== UTILS ========================
def send_typing_action(context: CallbackContext, chat_id: int):
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(1)

def get_reply_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Catfact \U0001F431"), KeyboardButton("Dog \U0001F436")],
        [KeyboardButton("Bored \U0001F3B2"), KeyboardButton("Quote \U0001F4AC")],
        [KeyboardButton("Poke \U0001F3AE"), KeyboardButton("Ping \U0001F4E1")],
        [KeyboardButton("User \U0001F464"), KeyboardButton("Help \U0001F4DA")]
    ], resize_keyboard=True)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("\U0001F431 Cat Fact", callback_data='catfact'), InlineKeyboardButton("\U0001F436 Dog", callback_data='dog')],
        [InlineKeyboardButton("\U0001F3B2 Bored", callback_data='bored'), InlineKeyboardButton("\U0001F4AC Quote", callback_data='quote')],
        [InlineKeyboardButton("\U0001F3AE Pokémon", callback_data='poke'), InlineKeyboardButton("\U0001F30D Country Info", callback_data='country')],
        [InlineKeyboardButton("\U0001F464 Fake User", callback_data='user')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ======================== COMMANDS ========================
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    send_typing_action(context, chat_id)
    update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown', reply_markup=get_reply_keyboard())
    time.sleep(1)
    send_typing_action(context, chat_id)
    update.message.reply_text(INFO_MESSAGE, parse_mode='Markdown', reply_markup=main_menu())

def help_command(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    update.message.reply_text(HELP_TEXT, parse_mode='Markdown')

def ping(update: Update, context: CallbackContext):
    start_time = time.time()
    send_typing_action(context, update.effective_chat.id)
    msg = update.message.reply_text("\u23F3 Pinging...")
    latency = (time.time() - start_time) * 1000
    msg.edit_text(f"\U0001F4E1 Pong! Response time: `{int(latency)} ms`", parse_mode='Markdown')

def cat_fact(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    fact = requests.get("https://catfact.ninja/fact").json()["fact"]
    update.message.reply_text(f"\U0001F431 Cat Fact: {fact}")

def dog_pic(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    pic = requests.get("https://dog.ceo/api/breeds/image/random").json()["message"]
    update.message.reply_photo(pic)

def bored(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        activity = requests.get("https://www.boredapi.com/api/activity").json()["activity"]
        update.message.reply_text(f"\U0001F3B2 Try this: {activity}")
    except:
        update.message.reply_text("\u274C Couldn't fetch an activity right now. Try again later.")

def quote(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    data = requests.get("https://zenquotes.io/api/random").json()[0]
    update.message.reply_text(f"\U0001F4AC {data['q']}\n— {data['a']}", parse_mode='Markdown')

def poke(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    data = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu").json()
    types = ", ".join([t["type"]["name"] for t in data["types"]])
    update.message.reply_text(f"\U0001F3AE Pokémon: Pikachu\nTypes: {types}", parse_mode='Markdown')

def country(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        name = ' '.join(context.args)
        data = requests.get(f"https://restcountries.com/v3.1/name/{name}").json()[0]
        update.message.reply_text(
            f"\U0001F30D {data['name']['common']}\nCapital: {data['capital'][0]}\nRegion: {data['region']}\nPopulation: {data['population']}",
            parse_mode='Markdown')
    except:
        update.message.reply_text("\u274C Couldn’t find that country. Try another.")

def fake_user(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    data = requests.get("https://fakestoreapi.com/users/1").json()
    update.message.reply_text(
        f"\U0001F464 {data['name']['firstname']} {data['name']['lastname']}\n\U0001F4E7 {data['email']}\n\U0001F3E2 {data['address']['city']}",
        parse_mode='Markdown')

# ======================== BUTTON HANDLER ========================
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    cmd = query.data
    fake_update = Update(update.update_id, message=query.message)
    commands = {
        "catfact": cat_fact,
        "dog": dog_pic,
        "bored": bored,
        "quote": quote,
        "poke": poke,
        "country": lambda u, c: query.message.reply_text("\U0001F30D Use /country <name> to get info."),
        "user": fake_user
    }
    if cmd in commands:
        commands[cmd](fake_update, context)

# ======================== MAIN ========================
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("catfact", cat_fact))
    dp.add_handler(CommandHandler("dog", dog_pic))
    dp.add_handler(CommandHandler("bored", bored))
    dp.add_handler(CommandHandler("quote", quote))
    dp.add_handler(CommandHandler("poke", poke))
    dp.add_handler(CommandHandler("country", country))
    dp.add_handler(CommandHandler("user", fake_user))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://pwizardbot-1.onrender.com/{TOKEN}"
    )
    updater.idle()

if __name__ == '__main__':
    main()

# PWizard Bot: Enhanced version with interactive reply buttons, dynamic fake user, and cleaner UX

import os
import time
import logging
import requests
import random
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton, ChatAction, Message
)
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,
    CallbackQueryHandler, MessageHandler, Filters
)

# ========== CONFIG ==========
TOKEN = os.getenv("TOKEN", "8185936093:AAFeVtgngoz_fKo0a6LY-tYl8s4x6qlKFnU")
PORT = int(os.environ.get("PORT", "8442"))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ========== TEXTS ==========
WELCOME_MESSAGE = "\U0001F916 Welcome to *PWizard Bot!*"
INFO_MESSAGE = (
    "\u2728 I can show you fun facts, quotes, pics and more!\n\n"
    "Try:\n"
    "• /catfact – Cat trivia 🐱\n"
    "• /dog – Cute dog photo 🐶\n"
    "• /bored – What to do? 🎲\n"
    "• /quote – Inspiring quote 💬\n"
    "• /poke – Pokémon profile 🎮\n"
    "• /country <name> – Country details 🌍\n"
    "• /user – Random profile 👤\n"
    "• /ping – Check speed 📡\n"
    "• /help – How this works 📚"
)

# ========== UTILS ==========
def send_typing_action(context: CallbackContext, chat_id: int):
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(1)

def get_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["Catfact 🐱", "Dog 🐶"],
        ["Bored 🎲", "Quote 💬"],
        ["Poke 🎮", "Ping 📡"],
        ["User 👤", "Help 📚"]
    ], resize_keyboard=True)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🐱 Cat Fact", callback_data='catfact'), InlineKeyboardButton("🐶 Dog", callback_data='dog')],
        [InlineKeyboardButton("🎲 Bored", callback_data='bored'), InlineKeyboardButton("💬 Quote", callback_data='quote')],
        [InlineKeyboardButton("🎮 Pokémon", callback_data='poke'), InlineKeyboardButton("🌍 Country Info", callback_data='country')],
        [InlineKeyboardButton("👤 Fake User", callback_data='user')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== COMMAND HANDLERS ==========
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    send_typing_action(context, chat_id)
    update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown', reply_markup=get_reply_keyboard())
    time.sleep(1)
    send_typing_action(context, chat_id)
    update.message.reply_text(INFO_MESSAGE, parse_mode='Markdown', reply_markup=main_menu())

def help_command(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    update.message.reply_text(INFO_MESSAGE, parse_mode='Markdown')

def ping(update: Update, context: CallbackContext):
    start_time = time.time()
    send_typing_action(context, update.effective_chat.id)
    msg = update.message.reply_text("⏳ Pinging...")
    latency = (time.time() - start_time) * 1000
    msg.edit_text(f"📡 Pong! `{int(latency)} ms`", parse_mode='Markdown')

def cat_fact(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    fact = requests.get("https://catfact.ninja/fact").json()["fact"]
    update.message.reply_text(f"🐱 Cat Fact: {fact}")

def dog_pic(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    pic = requests.get("https://dog.ceo/api/breeds/image/random").json()["message"]
    update.message.reply_photo(pic)

def bored(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        activity = requests.get("https://www.boredapi.com/api/activity").json()["activity"]
        update.message.reply_text(f"🎲 Try this: {activity}")
    except:
        update.message.reply_text("❌ Couldn't fetch an activity right now.")

def quote(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    data = requests.get("https://zenquotes.io/api/random").json()[0]
    update.message.reply_text(f"💬 {data['q']}\n— {data['a']}", parse_mode='Markdown')

def poke(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    data = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu").json()
    types = ", ".join([t["type"]["name"] for t in data["types"]])
    update.message.reply_text(f"🎮 Pokémon: Pikachu\nTypes: {types}", parse_mode='Markdown')

def country(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        name = ' '.join(context.args)
        data = requests.get(f"https://restcountries.com/v3.1/name/{name}").json()[0]
        update.message.reply_text(
            f"🌍 {data['name']['common']}\nCapital: {data['capital'][0]}\nRegion: {data['region']}\nPopulation: {data['population']}",
            parse_mode='Markdown')
    except:
        update.message.reply_text("❌ Couldn’t find that country. Try another.")

def fake_user(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    user_id = random.randint(1, 10)
    data = requests.get(f"https://fakestoreapi.com/users/{user_id}").json()
    update.message.reply_text(
        f"👤 {data['name']['firstname']} {data['name']['lastname']}\n📧 {data['email']}\n🏙️ {data['address']['city']}",
        parse_mode='Markdown')

# ========== BUTTON HANDLER ==========
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    cmd = query.data
    dummy_msg = Message(message_id=0, date=None, chat=query.message.chat, from_user=query.from_user, text="/"+cmd)
    fake_update = Update(update.update_id, message=dummy_msg)
    command_map = {
        "catfact": cat_fact,
        "dog": dog_pic,
        "bored": bored,
        "quote": quote,
        "poke": poke,
        "country": lambda u, c: query.message.reply_text("🌍 Use /country <name>."),
        "user": fake_user
    }
    if cmd in command_map:
        command_map[cmd](fake_update, context)

# ========== TEXT COMMAND PARSER ==========
def handle_text_buttons(update: Update, context: CallbackContext):
    text_map = {
        "Catfact 🐱": cat_fact,
        "Dog 🐶": dog_pic,
        "Bored 🎲": bored,
        "Quote 💬": quote,
        "Poke 🎮": poke,
        "Ping 📡": ping,
        "User 👤": fake_user,
        "Help 📚": help_command,
    }
    text = update.message.text.strip()
    if text in text_map:
        # Delete user message after clicking
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        text_map[text](update, context)

# ========== MAIN ==========
def main():
    updater = Updater(TOKEN, use_context=True)
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
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_buttons))

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://pwizardbot-1.onrender.com/{TOKEN}"
    )
    updater.idle()

if __name__ == '__main__':
    main()

import os
import time
import logging
import requests
import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ChatAction
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# ======================== CONFIG ========================

TOKEN = os.getenv("TOKEN", "8185936093:AAFeVtgngoz_fKo0a6LY-tYl8s4x6qlKFnU")

# Logging to file
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("pwizard_bot.log"),
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
    "• /ping – Check bot status 📡\n"
    "• /help – How this bot works 📚\n\n"
    "🔽 Use the menu below to explore."
)
HELP_TEXT = INFO_MESSAGE

# ======================== MENUS ========================

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🐱 Cat Fact", callback_data="catfact"), InlineKeyboardButton("🐶 Dog", callback_data="dog")],
        [InlineKeyboardButton("🎲 Bored", callback_data="bored"), InlineKeyboardButton("💬 Quote", callback_data="quote")],
        [InlineKeyboardButton("🎮 Pokémon", callback_data="poke"), InlineKeyboardButton("🌍 Country Info", callback_data="country")],
        [InlineKeyboardButton("👤 Fake User", callback_data="user")]
    ]
    return InlineKeyboardMarkup(keyboard)

def bottom_menu():
    keyboard = [
        ["🐱 Cat Fact", "🐶 Dog"],
        ["💬 Quote", "🎲 Bored"],
        ["🎮 Pokémon", "🌍 Country"],
        ["👤 Fake User", "📡 Ping", "📚 Help"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ======================== UTILS ========================

def send_typing_action(context: CallbackContext, chat_id: int):
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(1)

# ======================== COMMANDS ========================

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    send_typing_action(context, chat_id)
    update.message.reply_text(WELCOME_MESSAGE, parse_mode="Markdown")
    time.sleep(1)
    send_typing_action(context, chat_id)
    update.message.reply_text(INFO_MESSAGE, parse_mode="Markdown", reply_markup=main_menu())
    update.message.reply_text("👇 Choose an option below", reply_markup=bottom_menu())

def help_command(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    update.message.reply_text(HELP_TEXT, parse_mode="Markdown")

def cat_fact(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    res = requests.get("https://catfact.ninja/fact").json()
    update.message.reply_text(f"🐱 Cat Fact:\n{res['fact']}")

def dog_pic(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    res = requests.get("https://dog.ceo/api/breeds/image/random").json()
    update.message.reply_photo(res["message"])

def bored(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        res = requests.get("https://www.boredapi.com/api/activity").json()
        update.message.reply_text(f"🎲 Try this: {res['activity']}")
    except:
        update.message.reply_text("😞 Couldn't fetch activity. Try again later.")

def quote(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    res = requests.get("https://zenquotes.io/api/random").json()
    quote = res[0]['q']
    author = res[0]['a']
    update.message.reply_text(f"💬 {quote}\n— {author}", parse_mode="Markdown")

def poke(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    res = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu").json()
    name = res["name"].title()
    types = ", ".join([t["type"]["name"] for t in res["types"]])
    update.message.reply_text(f"🎮 Pokémon: {name}\nTypes: {types}")

def country(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    try:
        name = " ".join(context.args)
        res = requests.get(f"https://restcountries.com/v3.1/name/{name}").json()[0]
        info = f"🌍 {res['name']['common']}\nCapital: {res['capital'][0]}\nRegion: {res['region']}\nPopulation: {res['population']}"
        update.message.reply_text(info)
    except:
        update.message.reply_text("❌ Couldn’t find that country. Try another.")

def fake_user(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    res = requests.get("https://fakestoreapi.com/users/1").json()
    name = res["name"]
    update.message.reply_text(f"👤 {name['firstname']} {name['lastname']}\n📧 {res['email']}\n🏙️ {res['address']['city']}")

def ping(update: Update, context: CallbackContext):
    send_typing_action(context, update.effective_chat.id)
    now = datetime.datetime.utcnow()
    update.message.reply_text(f"📡 Pong! Bot is alive.\nUTC Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# ======================== BUTTON HANDLER ========================

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    command_map = {
        "catfact": cat_fact,
        "dog": dog_pic,
        "bored": bored,
        "quote": quote,
        "poke": poke,
        "country": lambda u, c: u.callback_query.message.reply_text("🌍 Use /country <name>"),
        "user": fake_user
    }

    if data in command_map:
        dummy_update = Update(update.update_id, message=query.message)
        command_map[data](dummy_update, context)

# ======================== TEXT BUTTON HANDLER ========================

def handle_menu_buttons(update: Update, context: CallbackContext):
    text = update.message.text
    mapping = {
        "🐱 Cat Fact": cat_fact,
        "🐶 Dog": dog_pic,
        "💬 Quote": quote,
        "🎲 Bored": bored,
        "🎮 Pokémon": poke,
        "🌍 Country": lambda u, c: u.message.reply_text("🌍 Use /country <name>"),
        "👤 Fake User": fake_user,
        "📚 Help": help_command,
        "📡 Ping": ping
    }

    if text in mapping:
        mapping[text](update, context)

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
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_buttons))

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://pwizardbot.onrender.com/{TOKEN}"
    )
    updater.idle()
    
if __name__ == '__main__':
    main()

import os
import time
import logging
import requests
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, MessageHandler, filters
)

# ======================== CONFIG ========================

TOKEN = os.getenv("TOKEN", "8185936093:AAFeVtgngoz_fKo0a6LY-tYl8s4x6qlKFnU")

# Logging to both file and console
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

WELCOME_MESSAGE = "✫ Welcome to *PWizard Bot!*"
INFO_MESSAGE = (
    "\n✨ I can show you random fun facts, dog pics, motivational quotes, country details and more.\n\n"
    "🧰 Try these commands:\n"
    "• Cat Fact 🐱\n"
    "• Dog 🐶\n"
    "• Bored 🎲\n"
    "• Quote 💬\n"
    "• Pokémon 🎮\n"
    "• Country Info 🌍\n"
    "• Fake User 👤\n"
    "• Ping 📶\n"
)

HELP_TEXT = (
    "\U0001F4DA *How to Use This Bot:*\n\n"
    "Send any of the following keywords or use the menu:\n"
    "• Cat Fact\n"
    "• Dog\n"
    "• Bored\n"
    "• Quote\n"
    "• Pokémon\n"
    "• Country <name>\n"
    "• Fake User\n"
    "• Ping"
)

# ======================== UTILS ========================

async def send_typing_action(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await asyncio.sleep(1)

# ======================== COMMAND HANDLERS ========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')
    await send_typing_action(context, update.effective_chat.id)
    await update.message.reply_text(INFO_MESSAGE, parse_mode='Markdown', reply_markup=main_menu())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    await update.message.reply_text(HELP_TEXT, parse_mode='Markdown')

async def cat_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    response = requests.get("https://catfact.ninja/fact").json()
    await update.message.reply_text(f"🐱 Cat Fact: {response['fact']}")

async def dog_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    response = requests.get("https://dog.ceo/api/breeds/image/random").json()
    await update.message.reply_photo(response['message'])

async def bored(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    try:
        response = requests.get("https://www.boredapi.com/api/activity").json()
        await update.message.reply_text(f"🎲 Try this: {response['activity']}")
    except:
        await update.message.reply_text("\ud83d\ude1e Couldn't fetch an activity right now. Try again later.")

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    response = requests.get("https://zenquotes.io/api/random").json()
    quote = response[0]['q']
    author = response[0]['a']
    await update.message.reply_text(f"💬 {quote}\n— {author}", parse_mode='Markdown')

async def poke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    response = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu").json()
    name = response['name'].title()
    types = ', '.join([t['type']['name'] for t in response['types']])
    await update.message.reply_text(f"🎮 Pokémon: {name}\nTypes: {types}", parse_mode='Markdown')

async def country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    try:
        name = ' '.join(context.args)
        response = requests.get(f"https://restcountries.com/v3.1/name/{name}").json()[0]
        info = f"🌍 {response['name']['common']}\nCapital: {response['capital'][0]}\nRegion: {response['region']}\nPopulation: {response['population']}"
        await update.message.reply_text(info, parse_mode='Markdown')
    except:
        await update.message.reply_text("\u274c Couldn’t find that country. Try another.")

async def fake_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    response = requests.get("https://fakestoreapi.com/users/1").json()
    name = response['name']
    await update.message.reply_text(
        f"👤 {name['firstname']} {name['lastname']}\n📧 {response['email']}\n🏣 {response['address']['city']}",
        parse_mode='Markdown')

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_action(context, update.effective_chat.id)
    start_time = time.time()
    await update.message.reply_text("⏳ Pinging...")
    latency = round((time.time() - start_time) * 1000)
    await update.message.reply_text(f"🔌 Pong! Response Time: {latency}ms")

# ======================== MENU ========================

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🐱 Cat Fact", callback_data='catfact'), InlineKeyboardButton("🐶 Dog", callback_data='dog')],
        [InlineKeyboardButton("🎲 Bored", callback_data='bored'), InlineKeyboardButton("💬 Quote", callback_data='quote')],
        [InlineKeyboardButton("🎮 Pokémon", callback_data='poke'), InlineKeyboardButton("🌍 Country Info", callback_data='country')],
        [InlineKeyboardButton("👤 Fake User", callback_data='user'), InlineKeyboardButton("📶 Ping", callback_data='ping')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    command_map = {
        'catfact': cat_fact,
        'dog': dog_pic,
        'bored': bored,
        'quote': quote,
        'poke': poke,
        'country': lambda u, c: u.callback_query.message.reply_text("🌍 Use /country <name> to get info."),
        'user': fake_user,
        'ping': ping
    }

    if data in command_map:
        dummy_update = Update(update.update_id, callback_query=query)
        await command_map[data](update, context)

async def handle_menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    match text:
        case "cat fact": await cat_fact(update, context)
        case "dog": await dog_pic(update, context)
        case "bored": await bored(update, context)
        case "quote": await quote(update, context)
        case "pokémon": await poke(update, context)
        case "ping": await ping(update, context)
        case "fake user": await fake_user(update, context)
        case _: await update.message.reply_text("❓ Unknown command. Use /help")

# ======================== MAIN ========================

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("catfact", cat_fact))
    app.add_handler(CommandHandler("dog", dog_pic))
    app.add_handler(CommandHandler("bored", bored))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("poke", poke))
    app.add_handler(CommandHandler("country", country))
    app.add_handler(CommandHandler("user", fake_user))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_buttons))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())

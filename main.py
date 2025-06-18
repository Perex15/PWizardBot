import os
TOKEN = os.getenv("8185936093:AAFeVtgngoz_fKo0a6LY-tYl8s4x6qlKFnU")

import time import logging from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.constants import ChatAction from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler import requests

Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) logger = logging.getLogger(name)

======================== BOT COMMANDS ==========================

WELCOME_MESSAGE = """ 🤖 Welcome to PWizard Bot! """

INFO_MESSAGE = """ ✨ I can show you random fun facts, dog pics, motivational quotes, country details and more.

🧰 Try these commands: • /catfact – Cat trivia 🐱 • /dog – Cute dog photo 🐶 • /bored – What to do? 🎲 • /quote – Inspiring quote 💬 • /poke – Pokémon profile 🎮 • /country <name> – Country details 🌍 • /user – Random profile 👤 • /help – How this bot works 📚

🔽 Use the menu below to explore. """

HELP_TEXT = """ 📚 How to Use This Bot:

Here’s a list of things I can do:

• /catfact – Fun cat trivia. • /dog – Sends a dog photo. • /bored – Suggests a random activity. • /quote – Motivational quote. • /poke – Shows Pokémon info. • /country <name> – Country facts. • /user – Generates a random profile.

You can also tap the buttons in the menu! """

======================== HANDLERS ============================

def send_typing_action(context: CallbackContext, chat_id: int): context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING) time.sleep(1)

def start(update: Update, context: CallbackContext): send_typing_action(context, update.effective_chat.id) update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown') time.sleep(1) send_typing_action(context, update.effective_chat.id) update.message.reply_text(INFO_MESSAGE, parse_mode='Markdown', reply_markup=main_menu())

def help_command(update: Update, context: CallbackContext): send_typing_action(context, update.effective_chat.id) update.message.reply_text(HELP_TEXT, parse_mode='Markdown')

def cat_fact(update: Update, context: CallbackContext): send_typing_action(context, update.effective_chat.id) response = requests.get("https://catfact.ninja/fact").json() update.message.reply_text(f"🐱 Cat Fact: {response['fact']}")

def dog_pic(update: Update, context: CallbackContext): send_typing_action(context, update.effective_chat.id) response = requests.get("https://dog.ceo/api/breeds/image/random").json() update.message.reply_photo(response['message'])

def bored(update: Update, context: CallbackContext): send_typing_action(context, update.effective_chat.id) response = requests.get("https://www.boredapi.com/api/activity").json() update.message.reply_text(f"🎲 Try this: {response['activity']}")

def quote(update: Update, context: CallbackContext): send_typing_action(context, update.effective_chat.id) response = requests.get("https://api.quotable.io/random").json() update.message.reply_text(f"💬 {response['content']}\n— {response['author']}", parse_mode='Markdown')

def poke(update: Update, context: CallbackContext): send_typing_action(context, update.effective_chat.id) response = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu").json() name = response['name'].title() types = ', '.join([t['type']['name'] for t in response['types']]) update.message.reply_text(f"🎮 Pokémon: {name}\nTypes: {types}", parse_mode='Markdown')

def country(update: Update, context: CallbackContext): send_typing_action(context, update.effective_chat.id) try: name = ' '.join(context.args) response = requests.get(f"https://restcountries.com/v3.1/name/{name}").json()[0] country_info = f"🌍 {response['name']['common']}\nCapital: {response['capital'][0]}\nRegion: {response['region']}\nPopulation: {response['population']}" update.message.reply_text(country_info, parse_mode='Markdown') except: update.message.reply_text("❌ Couldn’t find that country. Try another.")

def fake_user(update: Update, context: CallbackContext): send_typing_action(context, update.effective_chat.id) response = requests.get("https://randomuser.me/api/").json()['results'][0] name = response['name'] update.message.reply_text( f"👤 {name['title']} {name['first']} {name['last']}\n📧 {response['email']}\n🌍 {response['location']['country']}", parse_mode='Markdown')

======================== MENU SYSTEM ==========================

def main_menu(): keyboard = [ [InlineKeyboardButton("🐱 Cat Fact", callback_data='catfact'), InlineKeyboardButton("🐶 Dog", callback_data='dog')], [InlineKeyboardButton("🎲 Bored", callback_data='bored'), InlineKeyboardButton("💬 Quote", callback_data='quote')], [InlineKeyboardButton("🎮 Pokémon", callback_data='poke'), InlineKeyboardButton("🌍 Country Info", callback_data='country')], [InlineKeyboardButton("👤 Fake User", callback_data='user')], ] return InlineKeyboardMarkup(keyboard)

def button_handler(update: Update, context: CallbackContext): query = update.callback_query query.answer() dummy_update = Update(update.update_id, message=query.message) dummy_context = CallbackContext.from_update(dummy_update, context.dispatcher) command_map = { 'catfact': cat_fact, 'dog': dog_pic, 'bored': bored, 'quote': quote, 'poke': poke, 'country': lambda u, c: u.message.reply_text("🌍 Use /country <name> to get info."), 'user': fake_user } if query.data in command_map: command_map[query.data](dummy_update, dummy_context)

======================== MAIN BOT =============================

def main(): # Replace '8185936093:AAFeVtgngoz_fKo0a6LY-tYl8s4x6qlKFnU' with your actual bot token updater = Updater("8185936093:AAFeVtgngoz_fKo0a6LY-tYl8s4x6qlKFnU") dp = updater.dispatcher

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

updater.start_polling()
updater.idle()

if name == 'main': main()
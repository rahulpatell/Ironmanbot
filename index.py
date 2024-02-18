import os
from io import BytesIO
from queue import Queue

import requests
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ.get('6162361094:AAFQnk4ToxfUBpGOaxr423AxiEdCeTOdRE0')
MOVIE_DB_API_KEY = os.environ.get('a018699d15adb67c42c5e79029985f26e9c0d9b8')

bot = Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the movies bot!")

def search_movie(update: Update, context: CallbackContext):
    query = update.message.text.split(' ', 1)[1]
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={MOVIE_DB_API_KEY}&query={query}')
    data = response.json()
    if data['total_results'] > 0:
        movie = data['results'][0]
        keyboard = [[InlineKeyboardButton(text=movie['title'], url=f'https://www.themoviedb.org/movie/{movie["id"]}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f"Title: {movie['title']}\nRelease Date: {movie['release_date']}\nRating: {movie['vote_average']}", reply_markup=reply_markup)
    else:
        update.message.reply_text('No movies found. ')

def main():
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & Filters.command, search_movie))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

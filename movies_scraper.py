import os
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ.get('TELEGRAM_TOKEN', '6162361094:AAFQnk4ToxfUBpGOaxr423AxiEdCeTOdRE0')
MOVIE_DB_API_KEY = os.environ.get('MOVIE_DB_API_KEY', 'a018699d15adb67c42c5e79029985f26e9c0d9b8')

bot = Updater(token=TOKEN, use_context=True)
dispatcher = bot.dispatcher

def search_movies(query):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={MOVIE_DB_API_KEY}&query={query}'
    response = requests.get(url)
    data = response.json()
    return data['results']

def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={MOVIE_DB_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

def movie_result(update, context):
    query = update.inline_query.query
    movies = search_movies(query)
    if not movies:
        update.inline_query.answer([], cache_time=0)
        return

    results = []
    for movie in movies:
        movie_id = movie['id']
        title = movie['title']
        poster_path = movie['poster_path']
        overview = movie['overview']

        movie_url = f'https://www.themoviedb.org/movie/{movie_id}'
        movie_details = get_movie_details(movie_id)
        release_date = movie_details['release_date']

        result_id = f'movie-{movie_id}'
        result_text = f'{title}\n{overview}\nRelease Date: {release_date}'
        result_article = InlineQueryResultArticle(
            id=result_id,
            title=title,
            input_message_content=InputTextMessageContent(result_text),
            thumb_url=f'https://image.tmdb.org/t/p/w500{poster_path}',
            url=movie_url
        )
        results.append(result_article)

    update.inline_query.answer(results, cache_time=0)

def main():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(InlineQueryHandler(movie_result))

    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()

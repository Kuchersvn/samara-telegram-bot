import os
import telebot
from telebot import types
import database

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Environment variable TOKEN is not set")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    databas.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    bot.send_message(message.chat.id, "Привет! Я расскажу тебе о достопримечательностях Самары. Напиши 'Привет'.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.lower() == "привет":
        keyboard = types.InlineKeyboardMarkup()
        for place in databas.get_places():
            keyboard.add(types.InlineKeyboardButton(text=place[1], callback_data=f"place_{place[0]}"))
        bot.send_message(message.chat.id, "Выбери достопримечательность:", reply_markup=keyboard)
    elif message.text.lower() == "/favorites":
        favorites = databas.get_favorites(message.from_user.id)
        if favorites:
            text = "\n\n".join([f"{f[0]} — {f[1]}" for f in favorites])
            bot.send_message(message.chat.id, f"Твои избранные места:\n\n{text}")
        else:
            bot.send_message(message.chat.id, "У тебя пока нет избранных достопримечательностей.")
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши 'Привет'.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('place_'))
def callback_place(call):
    place_id = int(call.data.split('_')[1])
    conn = databas.conn
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM places WHERE id=?", (place_id,))
    place = cursor.fetchone()
    if place:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Добавить в избранное", callback_data=f"fav_{place_id}"))
        with open(place[3], 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=f"{place[1]}\n\n{place[2]}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('fav_'))
def callback_favorite(call):
    place_id = int(call.data.split('_')[1])
    databas.add_favorite(call.from_user.id, place_id)
    bot.send_message(call.message.chat.id, "✅ Добавлено в избранное!")

bot.polling(none_stop=True)

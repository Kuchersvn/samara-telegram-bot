import os
import telebot
from telebot import types
import database
import requests

# 🔑 Твои ключи
TOKEN = "8240275661:AAFXDbOJj8Kqw0cTJKqDZJWSS9BXE7i-E_A"
YANDEX_API_KEY = "demo_yandex_weather_api_key_ca6d09349ba0"

bot = telebot.TeleBot(TOKEN)


# 🧭 Главное меню (нижние кнопки)
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🏙 Достопримечательности", "⭐ Избранное")
    keyboard.row("🌤 Погода", "🗺 Карта Самары", "ℹ️ Помощь")
    return keyboard


# 🔹 Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    database.add_user(message.from_user.id, message.from_user.username)
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я расскажу тебе о достопримечательностях Самары.\n\n"
        "Выбери действие ниже 👇",
        reply_markup=main_menu()
    )


# 🔹 Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.lower()

    # Достопримечательности
    if "достопримечательности" in text:
        places = database.get_places()
        if not places:
            bot.send_message(message.chat.id, "⚠️ В базе пока нет достопримечательностей.")
            return

        keyboard = types.InlineKeyboardMarkup()
        for place in places:
            # place = (id, name, description, photo_path, lat, lon)
            keyboard.add(types.InlineKeyboardButton(text=place[1], callback_data=f"place_{place[0]}"))

        bot.send_message(
            message.chat.id,
            "📍 Выбери достопримечательность:",
            reply_markup=keyboard
        )

    # Избранное
    elif "избранное" in text:
        favorites = database.get_favorites(message.from_user.id)
        if favorites:
            text = "\n\n".join([f"⭐ {f[0]} — {f[1]}" for f in favorites])
            bot.send_message(message.chat.id, f"Твои избранные места:\n\n{text}")
        else:
            bot.send_message(message.chat.id, "У тебя пока нет избранных мест 😔")

    # Погода
    elif "погода" in text:
        send_weather(message.chat.id)

    # Карта Самары
    elif "карта" in text:
        bot.send_message(
            message.chat.id,
            "🗺 Вот карта Самары в Google Maps:\nhttps://www.google.com/maps/place/Самара"
        )

    # Помощь
    elif "помощь" in text:
        bot.send_message(
            message.chat.id,
            "ℹ️ Я бот-гид по Самаре!\n\n"
            "Доступные кнопки:\n"
            "🏙 Достопримечательности — список интересных мест\n"
            "⭐ Избранное — твои сохранённые места\n"
            "🌤 Погода — текущая погода в Самаре\n"
            "🗺 Карта Самары — откроет карту города"
        )

    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю 😅\nВыбери пункт меню ниже.", reply_markup=main_menu())


# 🔹 Callback — при выборе достопримечательности
@bot.callback_query_handler(func=lambda call: call.data.startswith('place_'))
def callback_place(call):
    place_id = int(call.data.split('_')[1])
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM places WHERE id=?", (place_id,))
    place = cursor.fetchone()

    if place:
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("⭐ В избранное", callback_data=f"fav_{place_id}"),
            types.InlineKeyboardButton("📍 Открыть на карте", url=f"https://www.google.com/maps?q={place[4]},{place[5]}")
        )

        if place[3] and os.path.exists(place[3]):
            with open(place[3], 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=f"{place[1]}\n\n{place[2]}", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, f"{place[1]}\n\n{place[2]}", reply_markup=markup)

    else:
        bot.send_message(call.message.chat.id, "⚠️ Не удалось найти информацию о месте.")


# 🔹 Добавление в избранное
@bot.callback_query_handler(func=lambda call: call.data.startswith('fav_'))
def callback_favorite(call):
    place_id = int(call.data.split('_')[1])
    database.add_favorite(call.from_user.id, place_id)
    bot.send_message(call.message.chat.id, "✅ Добавлено в избранное!")


# 🔹 Показ погоды
def send_weather(chat_id):
    try:
        url = "https://api.weather.yandex.ru/v2/forecast"
        params = {"lat": 53.1959, "lon": 50.1008, "lang": "ru_RU"}
        headers = {"X-Yandex-Weather-Key": YANDEX_API_KEY}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        temp = data["fact"]["temp"]
        feels_like = data["fact"]["feels_like"]
        condition = data["fact"]["condition"]

        conditions = {
            "clear": "☀️ ясно",
            "partly-cloudy": "🌤 переменная облачность",
            "cloudy": "☁️ облачно",
            "overcast": "🌥 пасмурно",
            "rain": "🌧 дождь",
            "snow": "❄️ снег",
        }

        text = (
            f"🌤 Погода в Самаре:\n\n"
            f"Температура: {temp}°C\n"
            f"Ощущается как: {feels_like}°C\n"
            f"Состояние: {conditions.get(condition, condition)}"
        )
        bot.send_message(chat_id, text)

    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Не удалось получить погоду.\nОшибка: {e}")


# 🔹 Запуск
bot.polling(none_stop=True)

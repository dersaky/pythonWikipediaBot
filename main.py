import telebot
from telebot import types
import wikipedia
import requests
from bs4 import BeautifulSoup

TOKEN = "7083317155:AAHqNoVWpGkUCfKtRZMf11c8lob9yiBkSJg"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Меню")
    markup.add(item1)
    user_name = message.from_user.first_name
    bot.reply_to(message, f"Привіт {user_name}! Я бот з штучним інтелектом. Просто надішлі мені слово або фразу, про яку хочеш дізнатися.")

@bot.message_handler(func=lambda message: message.text == "Меню")
def send_menu(message):
    bot.send_message(message.chat.id, text="Test")

@bot.message_handler(func=lambda message: True)
def send_info_from_wikipedia(message):
    try:
        wikipedia.set_lang("uk")
        search_result = wikipedia.summary(message.text)
        bot.reply_to(message, search_result)

        page_url = wikipedia.page(message.text).url

        image_url = get_first_image_from_wikipedia(page_url)

        if image_url:
            bot.send_photo(message.chat.id, image_url)
        else:
            bot.reply_to(message, text="Нема такого фото")

    except wikipedia.exceptions.DisambiguationError as e:
        bot.reply_to(message, f"Уточніть ваш запит. Можливо, ви мали на увазі: {','.join(e.options)}")
    except wikipedia.exceptions.PageError:
        bot.reply_to(message, "Інформація про ваш запит не знайдена.")
    except Exception as e:
        bot.reply_to(message, f"Виникла помилка: {str(e)}")

def get_first_image_from_wikipedia(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_element = soup.find('img')
    if image_element and 'src' in image_element.attrs:
        image_url = image_element['src']
        if image_url.startswith("//"):
            image_url = "https:" + image_url
        return image_url
    return None

bot.polling(non_stop=True)
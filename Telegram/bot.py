import os
import telebot
from telebot import types
from data_setup import DataSetup
from MappingData.data_loader import DataLoader
from geopy.distance import geodesic
from server_queries import ServerConnection
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

awaiting_input = {}


def generate_markup(buttons):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


def handle_top_hotels(callback_data, message, hotels_list):
    try:
        number = int(message.text)
        sorted_hotels = sorted(hotels_list, key=lambda x: x.get('price', float('inf')),
                               reverse=(callback_data == 'top_expensive'))
        top_hotels = sorted_hotels[:number]
        response = '\n'.join([f"{hotel['name']} - {hotel['price']}, {hotel['website_https']}" for hotel in top_hotels])
        bot.send_message(message.chat.id, response)
    except ValueError:
        bot.send_message(message.chat.id, 'Please enter a valid number.')


def handle_distance_between_hotels(message, hotels_list):
    try:
        hotel_names = message.text.split(',')
        if len(hotel_names) != 2:
            bot.send_message(message.chat.id, "Please provide exactly two hotel names separated by a comma.")
            return

        hotel1 = next(
            (hotel for hotel in hotels_list if hotel['name'].strip().lower() == hotel_names[0].strip().lower()), None)
        hotel2 = next(
            (hotel for hotel in hotels_list if hotel['name'].strip().lower() == hotel_names[1].strip().lower()), None)

        if not hotel1 or not hotel2:
            bot.send_message(message.chat.id,
                             "One or both of the hotels could not be found. Please check the names and try again.")
            return

        coord1 = (hotel1['coordinates'][0], hotel1['coordinates'][1])
        coord2 = (hotel2['coordinates'][0], hotel2['coordinates'][1])
        distance = geodesic(coord1, coord2).kilometers
        bot.send_message(message.chat.id,
                         f"The distance between {hotel1['name']} and {hotel2['name']} is {distance:.2f} kilometers.")

    except Exception as e:
        logger.error(f"Error calculating distance: {str(e)}")
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    buttons = [
        types.InlineKeyboardButton('List of calculations', callback_data='calculations'),
        types.InlineKeyboardButton('List of hotels', callback_data='hotels'),
        types.InlineKeyboardButton('List of sights', callback_data='attractions'),
        types.InlineKeyboardButton('Distribution of Hotel Price Categories', callback_data='statistics')
    ]
    markup = generate_markup(buttons)
    bot.send_message(message.chat.id, "Welcome to the Hotel Bot! Please choose an option:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.chat.id in awaiting_input)
def handle_input(message):
    callback_data = awaiting_input.pop(message.chat.id)
    hotels_loader = DataLoader('../JsonData/hotels_data.json')
    hotels_list = hotels_loader.load_data()

    if callback_data in ['top_expensive', 'top_cheapest']:
        handle_top_hotels(callback_data, message, hotels_list)
    elif callback_data == 'distance':
        handle_distance_between_hotels(message, hotels_list)
    elif callback_data == 'shortest_route':
        # Handle the shortest route logic here
        pass


@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    ds = DataSetup()
    sc = ServerConnection('0.0.0.0', 8888)
    sc.connect()

    if callback.data == 'hotels':
        xlsx_file_path = ds.generate_excel_file(ds.get_hotels_names())
        with open(xlsx_file_path, 'rb') as xlsx_file:
            bot.send_message(callback.message.chat.id, 'List of hotels')
            bot.send_document(callback.message.chat.id, xlsx_file)

    elif callback.data == 'attractions':
        xlsx_file_path = ds.generate_excel_file(ds.get_sights_names())
        with open(xlsx_file_path, 'rb') as xlsx_file:
            bot.send_message(callback.message.chat.id, 'List of attractions')
            bot.send_document(callback.message.chat.id, xlsx_file)

    elif callback.data == 'calculations':
        buttons = [
            types.InlineKeyboardButton('Price median', callback_data='median'),
            types.InlineKeyboardButton('Distance between locations', callback_data='distance'),
            types.InlineKeyboardButton('Standard deviation', callback_data='std_deviation'),
            types.InlineKeyboardButton('Average hotel price', callback_data='average_hotel_price'),
            types.InlineKeyboardButton('Top N Expensive Hotels', callback_data='top_expensive'),
            types.InlineKeyboardButton('Top N Cheapest Hotels', callback_data='top_cheapest'),
            types.InlineKeyboardButton('Average Hotel Rating', callback_data='average_rating'),
            types.InlineKeyboardButton('Correlation between Price and Rating', callback_data='correlation_price_rating')
        ]
        markup = generate_markup(buttons)
        bot.send_message(callback.message.chat.id, 'Choose the next action:', reply_markup=markup)

    elif callback.data == 'median':
        response = sc.send_message(b'median\n')
        bot.send_message(callback.message.chat.id, response)

    elif callback.data == 'distance':
        bot.send_message(callback.message.chat.id, 'Enter the names of hotels (Ex. HotelA, HotelB):')
        awaiting_input[callback.message.chat.id] = 'distance'

    elif callback.data == 'std_deviation':
        response = sc.send_message(b'std_deviation\n')
        bot.send_message(callback.message.chat.id, response)

    elif callback.data == 'average_hotel_price':
        response = sc.send_message(b'average_hotel_price\n')
        bot.send_message(callback.message.chat.id, response)

    elif callback.data == 'top_expensive':
        bot.send_message(callback.message.chat.id, 'Enter the number of hotels:')
        awaiting_input[callback.message.chat.id] = 'top_expensive'

    elif callback.data == 'top_cheapest':
        bot.send_message(callback.message.chat.id, 'Enter the number of hotels:')
        awaiting_input[callback.message.chat.id] = 'top_cheapest'

    elif callback.data == 'average_rating':
        response = sc.send_message(b'average_rating\n')
        bot.send_message(callback.message.chat.id, response)

    elif callback.data == 'correlation_price_rating':
        response = sc.send_message(b'correlation_price_rating\n')
        bot.send_message(callback.message.chat.id, response)

    elif callback.data == 'shortest_route':
        bot.send_message(callback.message.chat.id, 'Enter the names of hotels (Ex. HotelA, HotelB):')
        awaiting_input[callback.message.chat.id] = 'shortest_route'

    elif callback.data == 'statistics':
        dl = DataLoader('../JsonData/hotels_data.json')
        hotels_data = dl.load_data()

        price_categories = {
            'Budget (< $100)': 0,
            'Mid-range ($100 - $300)': 0,
            'Luxury (> $300)': 0
        }

        for hotel in hotels_data:
            try:
                price_str = hotel.get('price', '').replace('$', '').replace(',', '')
                price = float(price_str)

                if price < 100:
                    price_categories['Budget (< $100)'] += 1
                elif 100 <= price <= 300:
                    price_categories['Mid-range ($100 - $300)'] += 1
                else:
                    price_categories['Luxury (> $300)'] += 1
            except ValueError:
                continue

        labels = price_categories.keys()
        sizes = price_categories.values()

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#1f77b4', '#ff7f0e', '#2ca02c'])
        plt.title('Distribution of Hotel Price Categories')

        note_text = """
            Budget: Price < $100
            Mid-range: $100 <= Price <= $300
            Luxury: Price > $300
            """
        plt.gcf().text(0.5, 0.02, note_text, ha='center', fontsize=12, bbox=dict(facecolor='lightgrey', alpha=0.5))

        image_path = './hotel_price_distribution.png'
        plt.savefig(image_path)

        with open(image_path, 'rb') as image_file:
            bot.send_photo(callback.message.chat.id, image_file, caption="Here's the hotel price distribution chart!")

        os.remove(image_path)


if __name__ == '__main__':
    bot.infinity_polling()

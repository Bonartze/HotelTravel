import os
import telebot
from telebot import types
from data_setup import DataSetup
from MappingData.data_loader import DataLoader
from geopy.distance import geodesic
from server_queries import ServerConnection

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

awaiting_input = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    calculations = types.InlineKeyboardButton('List of calculations', callback_data='calculations')
    hotels_list = types.InlineKeyboardButton('List of hotels', callback_data='hotels')
    sights_list = types.InlineKeyboardButton('List of sights', callback_data='attractions')
    shortest_route = types.InlineKeyboardButton('Shortest route', callback_data='shortest_route')
    markup.add(calculations, hotels_list, sights_list, shortest_route)
    bot.send_message(message.chat.id, "Welcome to the Hotel Bot! Please choose an option:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.chat.id in awaiting_input)
def handle_input(message):
    callback_data = awaiting_input.pop(message.chat.id)
    hotels_loader = DataLoader('../JsonData/hotels_data.json')
    hotels_list = hotels_loader.load_data()

    if callback_data == 'top_expensive':
        try:
            number = int(message.text)
            sorted_hotels = sorted(hotels_list, key=lambda x: x.get('price', 0), reverse=True)
            top_hotels = sorted_hotels[:number]
            response = '\n'.join(
                [f"{hotel['name']} - {hotel['price']}, {hotel['website_https']}" for hotel in top_hotels])
            bot.send_message(message.chat.id, response)
        except ValueError:
            bot.send_message(message.chat.id, 'Please enter a valid number.')

    elif callback_data == 'top_cheapest':
        try:
            number = int(message.text)
            sorted_hotels = sorted(hotels_list, key=lambda x: x.get('price', float('inf')))
            top_hotels = sorted_hotels[:number]
            response = '\n'.join(
                [f"{hotel['name']} - {hotel['price']}, {hotel['website_https']}" for hotel in top_hotels])
            bot.send_message(message.chat.id, response)
        except ValueError:
            bot.send_message(message.chat.id, 'Please enter a valid number.')
    elif callback_data == 'distance':
        try:
            hotel_names = message.text.split(',')
            if len(hotel_names) != 2:
                bot.send_message(message.chat.id, "Please provide exactly two hotel names separated by a comma.")
                return

            hotel1 = next(
                (hotel for hotel in hotels_list if hotel['name'].strip().lower() == hotel_names[0].strip().lower()),
                None)
            hotel2 = next(
                (hotel for hotel in hotels_list if hotel['name'].strip().lower() == hotel_names[1].strip().lower()),
                None)

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
            bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
    elif callback_data == 'shortest_route':
        pass


@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    ds = DataSetup()
    sc = ServerConnection('127.0.0.1', 8888)
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
        markup = types.InlineKeyboardMarkup(row_width=1)
        median = types.InlineKeyboardButton('Price median', callback_data='median')
        distance_between_locations = types.InlineKeyboardButton('Distance between locations', callback_data='distance')
        std_deviation = types.InlineKeyboardButton('Standard deviation', callback_data='std_deviation')
        average_price = types.InlineKeyboardButton('Average hotel price', callback_data='average_hotel_price')
        top_expensive = types.InlineKeyboardButton('Top N Expensive Hotels', callback_data='top_expensive')
        top_cheapest = types.InlineKeyboardButton('Top N Cheapest Hotels', callback_data='top_cheapest')
        average_rating = types.InlineKeyboardButton('Average Hotel Rating', callback_data='average_rating')
        correlation_price_rating = types.InlineKeyboardButton('Correlation between Price and Rating',
                                                              callback_data='correlation_price_rating')
        markup.add(median, distance_between_locations, std_deviation, average_price,
                   top_expensive, top_cheapest, average_rating, correlation_price_rating)

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


bot.infinity_polling()

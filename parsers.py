import requests
from bs4 import BeautifulSoup
from settings import booking_url, cities
import re
import json
from abc import ABC, abstractmethod
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


class Parser(ABC):
    @abstractmethod
    def parse_page(self, url):
        pass

    @abstractmethod
    def parse_pages(self):
        pass


class HotelsParse(Parser):
    def __init__(self):
        self.booking_start_page = requests.get(booking_url)
        self.booking_soup = BeautifulSoup(self.booking_start_page.text, 'html.parser')
        self.pattern = re.compile(r'/city/.+/.+\.html')
        self.booking_certain_page = None
        self.hotels = []
        self.geolocator = Nominatim(user_agent="hotel_locator")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)

    def parse_page(self, url):
        self.booking_certain_page = requests.get(url)
        soup = BeautifulSoup(self.booking_certain_page.text, 'html.parser')
        parse_page = soup.find_all('div', attrs={'class': 'f71bc5a839'})

        for data in parse_page:
            hotel_name = data.find('h3', attrs={'class': 'c91d26f0de e6314e676b b5138f45ca a465879fb1'}).text
            address = data.find('div', attrs={'class': 'eb2c6a4f4b a5cc9f664c b945536500 bfdd9a2a60'}).text
            description = data.find('p', attrs={'class': 'eb2c6a4f4b bc424e8a43'}).text
            price = data.find('span', attrs={'class': 'b0e4f44795'}).text

            location = self.geocode(hotel_name)
            coordinates = (location.latitude, location.longitude) if location else "Not found"

            self.hotels.append({
                'name': hotel_name,
                'address': address,
                'description': description,
                'price': price,
                'coordinates': coordinates
            })

    def parse_pages(self):
        for tag in cities:
            print('https://www.booking.com/city/' + tag + '.html')
            self.parse_page('https://www.booking.com/' + tag)

    def write_into_json(self):
        with open('JsonData/hotels_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.hotels, f, ensure_ascii=False, indent=4)


a = HotelsParse()
a.parse_pages()
a.write_into_json()

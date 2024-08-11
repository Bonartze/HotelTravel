import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from parser_template import Parser
from MappingData.settings import countries
import json


class SightsParser(Parser):
    def __init__(self):
        self.booking_certain_page = None
        self.sights = []
        self.geolocator = Nominatim(user_agent="sight_locator")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)

    def parse_page(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch the page {url}: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        parsed_page = soup.find_all('div', attrs={
            'class': 'cursor-pointer aon-card h-full w-full'})
        for data in parsed_page:
            try:
                name = data.find('h4', attrs={'class': 'text-xl font-semibold leading-5 tracking-wider'}).text
            except AttributeError:
                name = 'No name available'
            try:
                country = data.find('h3',
                                    attrs={'class': 'text-xs font-semibold uppercase leading-4 tracking-widest'}).text
            except AttributeError:
                country = 'No country available'
            try:
                preview_comment = data.find('div', attrs={
                    'class': 'font-ao-serif my-1 text-base font-light leading-snug sm:leading-5'}).text
            except AttributeError:
                preview_comment = 'No rate available'
            try:
                picture_https = data.find('img', attrs={'class': 'w-full bg-gray-100'}).get('src')
            except AttributeError:
                picture_https = None
            try:
                website_ref = data.find('figure', attrs={'class': 'relative block w-full'}).find('a').get('href')
            except AttributeError:
                website_ref = None
            coordinates = self.geocode(name)
            if coordinates:
                self.sights.append({'name': name,
                                    'preview_comment': preview_comment,
                                    'coordinates': (coordinates.latitude, coordinates.longitude),
                                    'picture_https': picture_https,
                                    'website_link': 'https://www.atlasobscura.com' + website_ref})
                # print(name, country, preview_comment, picture_https, f"https://www.atlasobscura.com{website_ref}",
                #      coordinates.latitude, coordinates.longitude)

    def parse_pages(self):
        base_url = "https://www.atlasobscura.com/things-to-do/"
        urls = [f"{base_url}{country}" for country, city in
                countries.items()]
        for url in urls:
            print(url)
            self.parse_page(url)

    def write_into_json(self):
        with open('../JsonData/attractions_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.sights, f, ensure_ascii=False, indent=4)


sp = SightsParser()
sp.parse_pages()
sp.write_into_json()

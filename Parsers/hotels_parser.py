import requests
from bs4 import BeautifulSoup
from MappingData.settings import cities
import json
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from parser_template import Parser


class HotelsParse(Parser):
    def __init__(self):
        self.booking_certain_page = None
        self.hotels = []
        self.geolocator = Nominatim(user_agent="hotel_locator")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)

    def parse_page(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch the page {url}: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        parsed_page = soup.find_all('div', attrs={'itemscope': True, 'itemtype': 'http://schema.org/Hotel',
                                                  'class': 'e01df12ddf'})

        for data in parsed_page:
            try:
                hotel_name = data.find('h3', class_='eb73dc0c10').text.strip()
            except AttributeError:
                hotel_name = 'No name available'

            try:
                address = data.find('div', itemprop='address').text.strip()
            except AttributeError:
                address = 'No address available'

            try:
                description = data.find('div', attrs={'itemprop': 'address'}).find_next('div').text
            except AttributeError:
                description = 'No description available'

            try:
                price_element = data.find('span', text='Price from').find_next('span')
                if price_element:
                    price = price_element.text.strip()
                else:
                    price = 'No price available'
            except AttributeError:
                price = 'No price available'

            try:
                image_tag = data.find('a', class_='e5d7e430ba')
                website_https = image_tag['href'] if image_tag else 'No website available'
            except AttributeError:
                website_https = 'No image available'

            try:
                hotel_evaluation = data.find('div', class_='a447b19dfd')
                if hotel_evaluation:
                    hotel_evaluation_text = hotel_evaluation.text.strip()
                else:
                    hotel_evaluation_text = 'No hotel evaluation available'
            except AttributeError:
                hotel_evaluation_text = 'No hotel evaluation available'

            try:
                preview_comment = data.find('div', class_='e2585683de a66926738c')
                if preview_comment:
                    preview_comment_text = preview_comment.text.strip()
                else:
                    preview_comment_text = 'No hotel evaluation available'
            except AttributeError:
                preview_comment_text = 'No hotel evaluation available'

            try:
                picture_https = data.find('img', class_='cb3263eccd bf474a744b aae67e6639 ba85973b8a')
                if picture_https:
                    picture_https = picture_https.get('src')
                else:
                    picture_https = 'No picture evaluation available'
            except AttributeError:
                picture_https = 'No picture evaluation available'

            if hotel_name != 'No name available' and address != 'No address available' and price != 'No price available':
                location = self.geocode(hotel_name)
                coordinates = (location.latitude, location.longitude) if location else "Not found"
                if coordinates != 'Not found':
                    description = description.replace('Show more', '')
                    description += '.' if description[-1] != '.' else ''
                    # print(f"Hotel Name: {hotel_name}")
                    # print(f"Address: {address}")
                    # print(f"Description: {description}")
                    # print(f"Price: {price}")
                    # print(f"Image: {picture_https}")
                    self.hotels.append({
                        'name': hotel_name,
                        'address': address,
                        'description': description,
                        'price': price,
                        'coordinates': coordinates,
                        'website_https': website_https,
                        'hotel_evaluation': hotel_evaluation_text,
                        'preview_comment': preview_comment_text,
                        'picture_https': picture_https
                    })

    def parse_pages(self):
        for tag in cities:
            url = f'https://www.booking.com/city/{tag}.html'
            print(url)
            self.parse_page(url)

    def write_into_json(self):
        with open('../JsonData/hotels_data_backup.json', 'w', encoding='utf-8') as f:
            json.dump(self.hotels, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    a = HotelsParse()
    a.parse_pages()
    a.write_into_json()

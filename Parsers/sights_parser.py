from parser_template import Parser
from MappingData.settings import cities
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


class SightsParser(Parser):
    def __init__(self):
        self.booking_certain_page = None
        self.sights = []
        self.geolocator = Nominatim(user_agent="hotel_locator")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)

    def parse_page(self, url):

    def parse_pages(self):
        for tag in cities:
            url = f'https://www.booking.com/attractions/city/{tag}.html'
            print(url)
            self.parse_page(url)


sp = SightsParser()
sp.parse_pages()

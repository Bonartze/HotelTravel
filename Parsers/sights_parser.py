from parser_template import Parser
from MappingData.settings import cities
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class SightsParser(Parser):
    def __init__(self):
        self.booking_certain_page = None
        self.sights = []
        self.geolocator = Nominatim(user_agent="sight_locator")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)
        options = Options()
        options.add_argument("--lang=en")
        self.driver = webdriver.Chrome(options=options)

    def parse_page(self, url):
        self.driver.get(url)

        el = self.driver.find_element(By.CSS_SELECTOR,
                                      "body > div:nth-child(1) > div:nth-child(2) > div > div.css-ngwlx1 > div > div > div:nth-child(1) > div > div.css-1egjanf > div > div > a")
        el.click()
        time.sleep(15)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        parsed_page = soup.find_all('li', attrs={
            'class': 'f9637b0646 fe20ba46fc'})
        for data in parsed_page:
            try:
                name = data.find('a', attrs={'class': 'css-6c5ifu'}).text
            except AttributeError:
                name = 'No name available'
            try:
                country = data.find('div', attrs={'class': 'css-1utx3w7'}).text
            except AttributeError:
                country = 'No country available'
            try:
                rate = data.find('span', attrs={'class': 'e2585683de css-35ezg3'}).text
            except AttributeError:
                rate = 'No rate available'
            try:
                picture_https = data.find('img', attrs={'class': 'css-17k46x'}).get('src')
            except AttributeError:
                picture_https = None
            coordinates = self.geocode(name)
            print(country, name, rate, picture_https, coordinates)


    def parse_pages(self):
        for tag in cities:
            url = f'https://www.booking.com/attractions/city/{tag}.html'
            print(url)
            self.parse_page(url)


sp = SightsParser()
sp.parse_pages()

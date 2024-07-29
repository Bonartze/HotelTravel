from parser_template import Parser
from MappingData.settings import cities
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SightsParser(Parser):
    def __init__(self):
        self.booking_certain_page = None
        self.sights = []
        self.geolocator = Nominatim(user_agent="hotel_locator")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)
        self.driver = webdriver.Firefox()

    def parse_page(self, url):
        self.driver.get(url)

        try:
            wait = WebDriverWait(self.driver, 10)
            see_all_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "See all recommended")))
            see_all_button.click()

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".some-selector")))

        except Exception as e:
            print(f"Failed to click 'See all recommended': {e}")
            return
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        parsed_page = soup.find_all('ul', attrs={
            'class': 'adc8292e09 ea1e323a59 cab35cf0da fbe4119cc7 f795ed9755 css-zq8daf e3471aba6c'})
        print(parsed_page)
        for data in parsed_page:
            print(data)
            try:
                name = data.find('a', attrs={'class': 'css-6c5ifu'}).text
            except AttributeError:
                name = 'No name available'
            try:
                coutry = data.find('div', attrs={'class': 'css-1utx3w7'}).text
            except AttributeError:
                coutry = 'No country available'
            try:
                rate = data.find('span', attrs={'class': 'e2585683de css-35ezg3'}).text
            except AttributeError:
                rate = 'No rate available'
            try:
                picture_https = data.find('img', attrs={'class': 'css-17k46x'}).get('src')
            except AttributeError:
                picture_https = None

            print(coutry, name, rate, picture_https)
            # name =
            # rate =
            # price =

    def parse_pages(self):
        for tag in cities:
            url = f'https://www.booking.com/attractions/city/{tag}.html'
            print(url)
            self.parse_page(url)


sp = SightsParser()
sp.parse_pages()

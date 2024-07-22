import streamlit as st
import webbrowser
from .data_loader import DataLoader
from .map_generator import MapGenerator


class Interface:
    def on_click_follow_link(self, selected_hotel):
        for entry in self.map_generator.data:
            if entry['name'] == selected_hotel:
                picture_https = entry['website_https']
                webbrowser.open(picture_https)
                break

    def __init__(self):
        data_loader = DataLoader('JsonData/hotels_data_backup.json')
        data = data_loader.load_data()
        self.map_generator = MapGenerator(data)
        cities_names = self.map_generator.get_city_names()

        st.set_page_config(layout="wide")
        col1, col2 = st.columns([1, 5])
        with col1:
            st.title('Filters')
            st.header("City")
            selected_city = st.selectbox(
                "Choose the city",
                cities_names,
                index=0,
                placeholder="Select a city...",
            )

            st.header("Price")
            min_price, max_price = st.slider(
                "Select a range of prices in hotels per night",
                0, 1000, (0, 1000))
            selected_hotel = st.selectbox("Choose the hotel", [entry['name'] for entry in data_loader.data], index=1,
                                          placeholder='Select a hotel...')
            st.button('Follow the link', on_click=self.on_click_follow_link, args=(selected_hotel,))
        with col2:
            st.header("Hotels Map")
            self.map_generator.generate_map(min_price, max_price, selected_city)

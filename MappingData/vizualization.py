import streamlit as st
import webbrowser
from .data_loader import DataLoader
from .map_generator import MapGenerator


class Interface:
    def __init__(self):
        data_loader = DataLoader('MappingData/hotels_data.json')
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

        with col2:
            st.header("Hotels Map")
            self.map_generator.generate_map(min_price, max_price, selected_city)

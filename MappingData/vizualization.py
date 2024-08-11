import streamlit as st
from .data_loader import DataLoader
from .map_generator import MapGenerator


class Interface:
    def on_click_follow_link(self, selected, entry_type):
        if entry_type == "hotel":
            for entry in self.map_generator.hotels_data:
                if entry['name'] == selected:
                    st.session_state.selected_hotel_link = entry['website_https']
                    break
        elif entry_type == "sight":
            for entry in self.map_generator.sights_data:
                if entry['name'] == selected:
                    st.session_state.selected_sight_link = entry['website_link']
                    break

    def __init__(self):
        data_loader_hotels = DataLoader('JsonData/hotels_data.json')
        data_loader_sights = DataLoader('JsonData/attractions_data.json')
        hotels_data = data_loader_hotels.load_data()
        sights_data = data_loader_sights.load_data()
        self.map_generator = MapGenerator(hotels_data, sights_data)
        cities_names = self.map_generator.get_city_names()

        st.set_page_config(layout="wide")
        col1, col2, col3 = st.columns([2, 5, 2])

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
            selected_hotel = st.selectbox("Choose the hotel", [entry['name'] for entry in data_loader_hotels.data],
                                          index=1,
                                          placeholder='Select a hotel...')
            st.button('Show the link', on_click=self.on_click_follow_link, args=(selected_hotel, "hotel"),
                      key='hotel_link_button')
            if 'selected_hotel_link' in st.session_state:
                st.markdown(
                    f"[Link to the page of {selected_hotel} on booking.com]({st.session_state.selected_hotel_link})",
                    unsafe_allow_html=True)

            selected_sight = st.selectbox("Choose the attraction", [entry['name'] for entry in data_loader_sights.data],
                                          index=1,
                                          placeholder='Select an attraction...')
            st.button('Show the link', on_click=self.on_click_follow_link, args=(selected_sight, "sight"),
                      key='sight_link_button')
            if 'selected_sight_link' in st.session_state:
                st.markdown(
                    f"[Link to the page of {selected_sight} on atlas obscura]({st.session_state.selected_sight_link})",
                    unsafe_allow_html=True)

        with col2:
            st.header("Hotels Map")
            self.map_generator.generate_map(min_price, max_price, selected_city)
        with col3:
            st.markdown("### Map Legend")
            st.markdown("""
                <div style='display: flex; align-items: center;'>
                    <div style='width: 20px; height: 20px; background-color: blue; margin-right: 10px;'></div> 
                    <span>Sights (Free attractions)</span>
                </div>
                <div style='display: flex; align-items: center; margin-top: 5px;'>
                    <div style='width: 20px; height: 20px; background-color: green; margin-right: 10px;'></div>
                    <span>Hotels (Lower price)</span>
                </div>
                <div style='display: flex; align-items: center; margin-top: 5px;'>
                    <div style='width: 20px; height: 20px; background-color: red; margin-right: 10px;'></div>
                    <span>Hotels (Higher price)</span>
                </div>
            """, unsafe_allow_html=True)

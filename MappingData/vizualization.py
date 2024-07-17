import json
import pandas as pd
import pydeck as pdk
import streamlit as st


class Vizualize:
    def __init__(self):
        self.data = None

    def get_coords(self):
        with open('hotels_info.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_city_names(self):
        names = sorted(set(
            name['address'].split(',')[-1].strip() if ',' in name['address'] else name['address'].split(' ')[-1].strip()
            for name in self.data))
        names.insert(0, 'All cities')
        return names

    def get_map(self, min_price, max_price, selected_city):
        data_df = {
            'name': [], 'latitude': [], 'longitude': [], 'price': [],
            'address': [], 'description': [], 'photos': [], 'reviews': []
        }

        for key in self.data:
            if 'coordinates' in key and key['coordinates'] != 'Not found':
                price_str = key['price'].replace('$', '').replace(',', '')
                try:
                    price = float(price_str)
                except ValueError:
                    continue

                if min_price <= price <= max_price and (
                        selected_city == 'All cities' or str(selected_city) in key['address']):
                    data_df['name'].append(key['name'])
                    data_df['latitude'].append(key['coordinates'][0])
                    data_df['longitude'].append(key['coordinates'][1])
                    data_df['price'].append(price)
                    data_df['address'].append(key['address'])
                    data_df['description'].append(key['description'])
                    data_df['photos'].append(key.get('photos', 'No photos available'))
                    data_df['reviews'].append(key.get('reviews', 'No reviews available'))

        df = pd.DataFrame(data_df)

        if df.empty:
            st.write("No hotels for the selected price range.")

        max_price = df['price'].max()
        min_price = df['price'].min()

        df['price_normalized'] = (df['price'] - min_price) / (max_price - min_price)

        def get_color(price_normalized):
            red = int(price_normalized * 255)
            green = int((1 - price_normalized) * 255)
            return [red, green, 0]

        df['color'] = df['price_normalized'].apply(get_color)
        height_expression = "price * 10"
        layer = pdk.Layer(
            'ColumnLayer',
            data=df,
            get_position=['longitude', 'latitude'],
            get_elevation=height_expression,
            elevation_scale=100,
            radius=500,
            get_fill_color='color',
            pickable=True,
            auto_highlight=True
        )

        if 'view_state' not in st.session_state:
            st.session_state.view_state = pdk.ViewState(
                latitude=df['latitude'].mean(),
                longitude=df['longitude'].mean(),
                zoom=2,
                pitch=50
            )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=st.session_state.view_state,
            tooltip={"text": "{name}\nPrice: ${price}"}
        )

        st.session_state.view_state = r.initial_view_state

        st.pydeck_chart(r, use_container_width=True)


class Interface:
    def __init__(self):
        self.deck_vizual = Vizualize()
        self.deck_vizual.get_coords()
        cities_names = self.deck_vizual.get_city_names()

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
            self.deck_vizual.get_map(min_price, max_price, selected_city)


a = Interface()

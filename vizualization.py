import json
import pandas as pd
import pydeck as pdk
import streamlit as st


class Vizualize:
    def __init__(self):
        self.data = None

    def get_coords(self):
        with open('JsonData/hotels_data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_map(self, min_price, max_price):
        data_df = {'name': [], 'latitude': [], 'longitude': [], 'price': []}

        for key in self.data:
            if 'coordinates' in key and key['coordinates'] != 'Not found':
                price_str = key['price'].replace('$', '').replace(',', '')
                try:
                    price = float(price_str)
                except ValueError:
                    continue  # Skip entries with invalid price format

                if min_price <= price <= max_price:
                    data_df['name'].append(key['name'])
                    data_df['latitude'].append(key['coordinates'][0])
                    data_df['longitude'].append(key['coordinates'][1])
                    data_df['price'].append(price)

        df = pd.DataFrame(data_df)

        if df.empty:
            st.write("No data to display for the selected price range.")
            return

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
            radius=2000,
            get_fill_color='color',
            pickable=True,
            auto_highlight=True
        )

        view_state = pdk.ViewState(
            latitude=df['latitude'].mean(),
            longitude=df['longitude'].mean(),
            zoom=10,
            pitch=50
        )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{name}\nPrice: ${price}"}
        )

        st.pydeck_chart(r, use_container_width=True)


class Interface:
    def __init__(self):
        self.deck_vizual = Vizualize()
        st.set_page_config(layout="wide")
        col1, col2 = st.columns([1, 6])
        with col1:
            st.header("Price Filter")
            min_price, max_price = st.slider(
                "Select a range of prices in hotels per night",
                0, 1000, (0, 1000))
        with col2:
            st.header("Hotels Map")
            self.deck_vizual.get_coords()
            self.deck_vizual.get_map(min_price, max_price)


a = Interface()

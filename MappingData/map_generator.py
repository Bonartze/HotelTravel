import pandas as pd
import pydeck as pdk
import streamlit as st


class MapGenerator:
    def __init__(self, hotels_data, sights_data):
        self.hotels_data = hotels_data
        self.sights_data = sights_data

    def get_city_names(self):
        names = sorted(set(
            name['address'].split(',')[-1].strip() if ',' in name['address'] else name['address'].split(' ')[-1].strip()
            for name in self.hotels_data))
        names.insert(0, 'All cities')
        return names

    def generate_map(self, min_price, max_price, selected_city):
        data_df = {'name': [], 'latitude': [], 'longitude': [], 'price': [], 'website_https': [],
                   'hotel_evaluation': [], 'preview_comment': [], 'picture_https': []}

        for key in self.hotels_data:
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
                    data_df['website_https'].append(key.get('website_https', 'No website available'))
                    data_df['hotel_evaluation'].append(key.get('hotel_evaluation', 'No hotel evaluation'))
                    data_df['preview_comment'].append(key.get('preview_comment', 'No hotel evaluation'))
                    data_df['picture_https'].append(key.get('picture_https', 'No picture available'))

        for sight in self.sights_data:
            if 'coordinates' in sight and sight['coordinates'] != 'Not found':
                if selected_city == 'All cities' or str(selected_city) in sight['address']:
                    data_df['name'].append(sight['name'])
                    data_df['latitude'].append(sight['coordinates'][0])
                    data_df['longitude'].append(sight['coordinates'][1])
                    data_df['price'].append(0)
                    data_df['website_https'].append(sight.get('website_link', 'No website available'))
                    data_df['hotel_evaluation'].append('Not evaluated')
                    data_df['preview_comment'].append(sight.get('preview_comment', 'No preview comment'))
                    data_df['picture_https'].append(sight.get('picture_https', 'No picture available'))

        df = pd.DataFrame(data_df)

        if df.empty:
            st.write("No hotels for the selected price range.")
            return

        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        valid_prices_df = df[df['price'].notna()]

        max_price = valid_prices_df['price'].max()
        min_price = valid_prices_df['price'].min()

        def get_color(price_normalized):
            if pd.isna(price_normalized) or price_normalized == 0:
                return [0, 150, 255]
            red = int(price_normalized * 255)
            green = int((1 - price_normalized) * 255)
            return [red, green, 0]

        df['price_normalized'] = df['price'].apply(
            lambda x: (x - min_price) / (max_price - min_price) if pd.notnull(x) and x != 0 else None
        )

        df['color'] = df['price_normalized'].apply(get_color)

        df['pseudo_price'] = df['price']

        df['price'] = df['price'].apply(lambda x: x + 100 if x == 0 else x)

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

        if 'view_state' not in st.session_state:
            st.session_state.view_state = pdk.ViewState(
                latitude=df['latitude'].mean(),
                longitude=df['longitude'].mean(),
                zoom=2,
                pitch=90
            )
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=st.session_state.view_state,
            tooltip={
                "html": "<b>{name}</b><br>Price: ${pseudo_price}<br>{hotel_evaluation}<br>Preview comment: {preview_comment}<br><img src='{picture_https}' width='100' height='100'>",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            },
            map_style='mapbox://styles/mapbox/light-v10'
        )

        st.pydeck_chart(r, use_container_width=True)

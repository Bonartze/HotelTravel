import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MappingData.data_loader import DataLoader


class DataSetup:
    def __init__(self):
        hotels_loader = DataLoader('../JsonData/hotels_data.json')
        sights_loader = DataLoader('../JsonData/attractions_data.json')
        self.hotels_list = hotels_loader.load_data()
        self.sights_list = sights_loader.load_data()

    def get_hotels_names(self):
        hotel_names = [hotel['name'] for hotel in self.hotels_list if 'name' in hotel]
        return hotel_names

    def get_sights_names(self):
        sights_names = [sight['name'][1:-1] for sight in self.sights_list if 'name' in sight]
        return sights_names

    def generate_excel_file(self, names):
        df = pd.DataFrame({'Hotel Names': names})
        excel_file_path = "list_names.xlsx"
        df.to_excel(excel_file_path, index=False)
        return excel_file_path

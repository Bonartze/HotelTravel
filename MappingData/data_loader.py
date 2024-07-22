import json


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        return self.data

import json


class JSONFileUtilities:

    def __init__(self):
        self.json_file = "unknown"

    def get_json(self, json_file):
        with open(json_file) as f:
            data = json.load(f)
        return data

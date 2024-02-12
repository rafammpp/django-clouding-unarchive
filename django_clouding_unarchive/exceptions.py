import json

class CloudingAPIError(Exception):
    def __init__(self, json_response):
        self.json_response = json_response
        self.message = json.dumps(json_response, indent=2)
        super().__init__(self.message)
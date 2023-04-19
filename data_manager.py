import requests

SHEETY_API = "https://api.sheety.co/327909c8a3bc8b16aef975bf629ae3fa/flightDeals/sheet1"
CUSTOMER_ENDPOINT = "https://api.sheety.co/327909c8a3bc8b16aef975bf629ae3fa/flightDeals/users"

class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_API)
        data = response.json()
        self.destination_data = data["sheet1"]
        return self.destination_data

    def update_destination_code(self):
    #POSTING TO SPREADSHEET
        for city in self.destination_data:
            new_data = {
                "sheet1": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_API}/{city['id']}",
                json=new_data
            )
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=CUSTOMER_ENDPOINT)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data

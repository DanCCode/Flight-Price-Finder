import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flight_data import FlightData
from data_manager import DataManager
from pprint import pprint

TEQUILA_API = "6pwTp-Ia1D_0SHh-p6eVgWrk72F4wIFo"
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TOMORROW_DATE = (datetime.today() + relativedelta(days=+1)).strftime('%d/%m/%Y')
ONE_WEEK = (datetime.today() + relativedelta(days=+7)).strftime('%d/%m/%Y')
FOUR_WEEKS = (datetime.today() + relativedelta(days=+28)).strftime('%d/%m/%Y')
SIX_MONTH_DATE = (datetime.today() + relativedelta(months=+6)).strftime('%d/%m/%Y')

headers = {
     "apikey": "6pwTp-Ia1D_0SHh-p6eVgWrk72F4wIFo",
 }

class FlightSearch:

    def get_destination_code(self, city_name):
        print("get destination codes triggered")
        query = {"term": city_name, "location_types": "city"}
        LOCATION_ENDPOINT = f"{TEQUILA_ENDPOINT}/locations/query"
        response = requests.get(url=LOCATION_ENDPOINT, params=query, headers=headers)
        response.raise_for_status()
        data = response.json()
        city_code = data["locations"][0]["code"]
        print(city_code)
        code = city_code
        return code

    def search_for_flights(self, origin_city_code, destination_city_code):
        print(f"Check flights triggered for {destination_city_code}")
        headers = {
            "apikey": "6pwTp-Ia1D_0SHh-p6eVgWrk72F4wIFo",
        }

        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": TOMORROW_DATE,
            "date_to": SIX_MONTH_DATE,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)
        response.raise_for_status()

        try:
            data = response.json()["data"][0]
            #pprint(data)
        except IndexError:

            query["max_stopovers"] = 1
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=headers,
                params=query,
            )
            response.raise_for_status()
            try:
                data = response.json()["data"][0]
                pprint(data)

                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][0]["cityTo"],
                    destination_airport=data["route"][0]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][1]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )

                print(f"{flight_data.destination_city}: £{flight_data.price}, via {flight_data.via_city}")
                #return flight_data

            except IndexError:
                print(f"No flights found for {destination_city_code}.")
                pass

        else:

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            #return flight_data


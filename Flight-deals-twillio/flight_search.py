import requests
from pprint import pprint
from flight_data import FlightData
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = ""
SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_data):
        city_name = city_data["city"]
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        header = {
            "apikey": TEQUILA_API_KEY,
        }
        query = {
            "term": city_name,
            "location_types": "city",
        }
        response = requests.get(url=location_endpoint, headers=header, params=query)
        city_code = response.json()["locations"][0]["code"]
        city_data["iataCode"] = city_code

    def check_flight(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {
            "apikey": TEQUILA_API_KEY,
        }
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=SEARCH_ENDPOINT, params=query, headers=headers)
        try:
            data = response.json()["data"][0]
            # pprint(data)
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            # query["max_stopovers"] = 1
            # response = requests.get(
            #     url=f"{SEARCH_ENDPOINT}",
            #     headers=headers,
            #     params=query,
            # )
            # try:
            #     data = response.json()["data"][0]
            #     # pprint(data)
            # except AttributeError:
            #     print(f"No direct flights found for {destination_city_code}.")
            # else:
            #     flight_data = FlightData(
            #         price=data["price"],
            #         origin_city=data["route"][0]["cityFrom"],
            #         origin_airport=data["route"][0]["flyFrom"],
            #         destination_city=data["route"][1]["cityTo"],
            #         destination_airport=data["route"][1]["flyTo"],
            #         out_date=data["route"][0]["local_departure"].split("T")[0],
            #         return_date=data["route"][2]["local_departure"].split("T")[0],
            #         stop_overs=1,
            #         via_city=data["route"][0]["cityTo"]
            #     )
            #     return flight_data
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
            return flight_data





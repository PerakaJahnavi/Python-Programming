import requests

"""Tequila username = PerakaJahnavi
password = Jaya2001"""
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/9ca5914e93c19bec83a4c1c0b467d794/flightsClub/users"

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def update_the_code(self, sheet_data):
        for city in sheet_data:
            id_number = city["id"]
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"https://api.sheety.co/9ca5914e93c19bec83a4c1c0b467d794/flightDeals/prices/{id_number}", json=new_data)

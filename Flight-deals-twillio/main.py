#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from datetime import datetime, timedelta


origin_city = "LON"
response = requests.get(url="https://api.sheety.co/9ca5914e93c19bec83a4c1c0b467d794/flightDeals/prices")
sheet_data = response.json()["prices"]
pprint(sheet_data)
flight_search = FlightSearch()
data_manager = DataManager()
notification_manager = NotificationManager()
for city_data in sheet_data:
    flight_search.get_destination_code(city_data)
#data_manager.update_the_code(sheet_data)

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(30 * 6))

for city in sheet_data:
    flight = flight_search.check_flight(origin_city,
                                        city["iataCode"],
                                        tomorrow,
                                        six_months_from_today)
    try:
        if flight.price < city["lowestPrice"]:
            message = f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}"
            if flight.stop_overs > 0:
                message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

            link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
            notification_manager.send_mail(message, link)
            notification_manager.send_alert(message)
    except AttributeError:
        continue







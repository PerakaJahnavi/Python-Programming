from twilio.rest import Client
import requests
import smtplib
auth_token = "74111715d8028aa465fb86d28d85d065"
account_sid = "AC10aa3d704f05f1678d332669575098d0"
USERS_ENDPOINT = "https://api.sheety.co/9ca5914e93c19bec83a4c1c0b467d794/flightsClub/users"
EMAIL = "panakaluperaka@gmail.com"
PASSWORD = "hyckjhinjkjzsrgn"


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(account_sid, auth_token)

    def send_alert(self, message):
        message = self.client.messages \
            .create(
            body=f"{message}",
            from_="+14248423699",
            to="+917075178988"
        )
        print(message.sid)

    def send_mail(self, message, link):
        response = requests.get(url=USERS_ENDPOINT)
        users = response.json()["users"]
        emails = [row["email"] for row in users]
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            for mail in emails:
                connection.sendmail(from_addr=EMAIL, to_addrs=mail, msg=f"Subject: Flights Club!\n\n{message}\nFlight_Link: {link}")




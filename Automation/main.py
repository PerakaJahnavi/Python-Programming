import smtplib
from datetime import datetime

my_email = "EMAIL"
password = "PASSCODE"

today = datetime.now().date()
week_days = ["2023-01-24", "2023-01-29", "2023-02-05", "2023-02-12", "2023-02-19"]

if str(today) in week_days:
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs=f"manager.campus.wipro.com", msg="Subject: Requesting Update\n\n"
                                                        "Respected manager sir, "
                                                                "I am Peraka Jahnavi, my resume number is ####### and my superset ID is #######. I have no update about joining after receiving PJP confirmation mail. I have learned python course i.e 100 days bootcamp in these days which will be helpful to the organization to work. So I think I am ready to do work . So I kindly request you to give any update on joining. "
                                                        "Thanking you.")
    print("Message Sent!")

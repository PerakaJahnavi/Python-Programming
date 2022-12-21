##################### Extra Hard Starting Project ######################
import smtplib
import random
import pandas
import datetime as dt

my_email = "panakaluperaka@gmail.com"
password = "hyckjhinjkjzsrgn"

# pythonanywhere: To run the task daily at the selected time
""" username = PerakaJahnavi
email = jahnaviperaka@gmail.com
password = Jaya@2001 """

# data = pandas.read_csv("birthdays.csv")

# def letter():
#     letter_num = random.randint(1, 3)
#     birthday_person = "Jaya"
#     with open(f"letter_templates/letter_{letter_num}.txt") as letter_content:
#         letter_to_send = letter_content.read()
#         letter_to_send = letter_to_send.replace("[NAME]", birthday_person)
#         return letter_to_send
#
#
# def send_wishes():
#     connection = smtplib.SMTP("smtp.gmail.com")
#     connection.starttls()
#     connection.login(user=my_email, password=password)
#     connection.sendmail(from_addr=my_email, to_addrs=to_address, msg=f"Subject: Happy Birthday\n\n{letter()}")
#
#
# now = dt.datetime.now()
# for month in data["month"]:
#     if month == now.month:
#         for day in data["day"]:
#             if day == now.day:
#                 send_wishes()


today = dt.datetime.now()
today_tuple = (today.month, today.day)
data = pandas.read_csv("birthdays.csv")
birthday_dict = {(data_row.month, data_row.day): data_row for (index, data_row) in data.iterrows()}
print(birthday_dict)

if today_tuple in birthday_dict:
    birthday_person = birthday_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])


connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=my_email, password=password)
try:
    connection.sendmail(from_addr=my_email, to_addrs=f"{birthday_person.email}", msg=f"Subject: Happy Birthday\n\n{contents}")
except NameError:
    print("No one Birthday today!")


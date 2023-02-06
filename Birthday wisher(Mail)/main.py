##################### Extra Hard Starting Project ######################
import smtplib
import random
import pandas
import datetime as dt

my_email = ""
password = ""


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


import requests
from bs4 import BeautifulSoup
import smtplib

my_email = ""
password = ""
to_me = ""
headers = {
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}
target_price = 40
pan_url = "https://www.amazon.com/Sensarte-Nonstick-Skillet-Omelette-Cookware/dp/B09G7644DK/ref=sr_1_4_sspa?adgrpid=1335908264276341&hvadid=83494525933127&hvbmt=bb&hvdev=c&hvlocphy=116074&hvnetw=o&hvqmt=b&hvtargid=kwd-83495271187051%3Aloc-90&hydadcr=4700_13164989&keywords=made+in+nonstick+frying+pan&qid=1662472968&sr=8-4-spons&psc=1"
response = requests.get(url=pan_url, headers=headers)
pan_info = response.text
print(pan_info)
soup = BeautifulSoup(pan_info, "html.parser")
current_price = soup.find(name="span", class_="a-price-whole").getText().strip(".")
print(current_price)

if int(current_price) < target_price:
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email,
                        to_addrs=to_me,
                        msg=f'Suject: Amazon Price Alert\n\nSENSARTE Nonstick Frying Pan Skillet with Lid, Swiss Granite Coating Omelette Pan with Cover, Healthy Cookware Chef\'s Pan with Top, PFOA Free (9.5" + Glass Lid) is at ${current_price} which is less than you expected.\n{pan_url}')


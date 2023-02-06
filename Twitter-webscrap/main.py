from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

PROMISED_DOWN = 150
PROMISED_UP = 10
TWITTER_EMAIL = "EMAIL_ID"
TWITTER_PASSWORD = "PASSWORD"


class InternetSpeedTwitterBot:
    def __init__(self):
        self.chrome_driver_path = "C:/Users/jahna/OneDrive/Desktop/Jahnavi/Development/chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/result/13650624438")
        self.down = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div[2]/span')
        self.up = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/span')
        print(f"down: {self.down.text}")
        print(f"up: {self.up.text}")

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/")
        time.sleep(15)
        sign_in = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div/span/span').click()
        time.sleep(10)
        twitter_username = self.driver.find_element(By.NAME, 'text')
        time.sleep(5)
        twitter_username.send_keys("USERNAME")
        time.sleep(5)
        twitter_username.send_keys(Keys.ENTER)


internet_speed_twitter_bot = InternetSpeedTwitterBot()
# internet_speed_twitter_bot.get_internet_speed()
internet_speed_twitter_bot.tweet_at_provider()


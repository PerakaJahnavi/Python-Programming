from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# notification_bar = driver.find_element(By.NAME, 'Turn On').click()
# driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', )


class InstaFollower:

    def __init__(self):
        self.chrome_driver_path = "C:/Users/jahna/OneDrive/Desktop/Jahnavi/Development/chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(20)
        self.login_number = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        self.login_number.send_keys("7075178988")
        time.sleep(5)
        self.password = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        self.password.send_keys("Janu@090601")
        time.sleep(5)
        self.login_button = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
        time.sleep(5)
        self.not_now = self.driver.find_element(By.CSS_SELECTOR, ".cmbtv button").click()
        time.sleep(15)
        self.notification = self.driver.find_element(By.CSS_SELECTOR, "._a9-z button")
        self.notification.click()

    def find_followers(self):
        self.driver.get("https://www.instagram.com/chefsteps/")
        time.sleep(30)
        self.followers = self.driver.find_element(By.XPATH, '//*[@id="mount_0_0_/p"]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/ul/li[2]/a')
        self.followers.click()
        # modal = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]')
        # for i in range(10):
        #     # In this case we're executing some Javascript, that's what the execute_script() method does.
        #     # The method can accept the script as well as a HTML element.
        #     # The modal in this case, becomes the arguments[0] in the script.
        #     # Then we're using Javascript to say: "scroll the top of the modal (popup) element by the height of the modal (popup)"
        #     self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
        #     time.sleep(2)

    def follow(self):
        pass


insta_follower = InstaFollower()
#insta_follower.login()
insta_follower.find_followers()
#insta_follower.follow()




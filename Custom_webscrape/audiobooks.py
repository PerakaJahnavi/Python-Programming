from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path = "C:/Users/jahna/OneDrive/Desktop/Jahnavi/Development/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get('https://www.audible.in/?ref=Adbl_ip_rdr_from_US&source_code=AUDTM002080318002F&ipRedirectFrom=US&ipRedirectOriginalURL=search%3Fkeywords%3Dbook%26node%3D18573211011')
time.sleep(5)

SCROLL_PAUSE_TIME = 5
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
print(last_height)


def down_scrolling():
    start = 0
    stop = 500
    scroll = True
    while scroll:
        # Scroll down to bottom
        driver.execute_script(f"window.scrollTo({start}, {stop});")
        temp = stop
        start = stop
        stop = 500 + temp
        print(stop)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        if stop >= last_height:
            break


def up_scrolling():
    start = last_height
    stop = start - 500
    scroll = True
    while scroll:
        # Scroll down to bottom
        driver.execute_script(f"window.scrollTo({start}, {stop});")
        temp = stop
        start = stop
        stop = temp - 500
        print(stop)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        if stop <= 500:
            break


down_scrolling()
up_scrolling()

search = driver.find_element(By.XPATH, '//*[@id="header-search"]')
search.send_keys("Harry Potter")
search.send_keys(Keys.ENTER)
time.sleep(5)
driver.find_element(By.XPATH, '//*[@id="product-list-a11y-skiplink-target"]/span/ul/li[1]/div/div[1]/div/div[2]/div/div/span/ul/li[1]/h3/a').click()
driver.find_element(By.CLASS_NAME, 'bc-button-text').click()
time.sleep(20)
driver.find_element(By.XPATH, '//*[@id="adbl-minerva-anon-sticky-buybox-trigger"]/span/a').click()
time.sleep(5)
mail = driver.find_element(By.NAME, 'email')
mail.send_keys("7075178988")
password = driver.find_element(By.NAME, 'password')
password.send_keys("Jaya@2001")
password.send_keys(Keys.ENTER)
time.sleep(5)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


chrome_driver_path = ""
driver = webdriver.Chrome(executable_path=chrome_driver_path)


def scrolling():
    SCROLL_PAUSE_TIME = 5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)
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
            driver.quit()
            break


driver.get("https://www.nba.com/stats")
# games = driver.find_element(By.XPATH, '//*[@id="nav-ul"]/li[1]/a')
# time.sleep(5)
# games.click()
# tickets = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[3]/nav/ul/li[3]')
# tickets.click()
# time.sleep(15)
# next_button = tickets.find_element(By.XPATH, '//*[@id="tickets_top_promo"]/div/div[3]/div[1]/a')
# actions = ActionChains(driver)
# actions.move_to_element(next_button).perform()
# time.sleep(20)
# next_button.click()
# driver.find_element(By.CSS_SELECTOR, '.featured-games .flex-matchup a img').click()
# time.sleep(5)
# driver.find_element(By.CSS_SELECTOR, ".tixbutton a").click()
# time.sleep(5)
# driver.find_element(By.XPATH, '//*[@id="tab--1"]/div/div/div[3]/div/div[2]/div/div[1]/div[2]/a').click()
watch = driver.find_element(By.XPATH, '//*[@id="nav-ul"]/li[3]/a')
time.sleep(5)
watch.click()
nba = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[3]/nav/ul/li[3]')
time.sleep(5)
nba.click()
nba.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[3]/div/div[2]/div/div/div/div[1]/div/div/a/div/div[1]').click()



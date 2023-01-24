from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import pandas as pd

chrome_driver_path = "C:/Users/jahna/OneDrive/Desktop/Jahnavi/Development/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get('https://steamdb.info/')
most_played = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[1]/div[1]')
most_played_games = most_played.find_elements(By.CLASS_NAME, 'css-truncate')
m_games = [game.text for game in most_played_games[1: ]]
game_info = ['Game', "App-ID", "Developer", "Release-Date"]
app = []
for i in range(2, len(m_games) + 1):
    most_played = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[1]/div[1]')
    game = most_played.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[1]/div[1]/table/tbody/tr[' + str(i) + ']/td[2]/a')
    game.click()
    time.sleep(5)
    app_id = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[1]/td[2]')
    developer = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[3]/td[2]')
    release_date = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div/div[2]/div[1]/table/tbody/tr[8]/td[2]')
    app.append({"Game": m_games[i-2],
                "App-ID": app_id.text,
                "Developer": developer.text,
                "Release-Date": release_date.text})
    driver.find_element(By.CLASS_NAME, 'header-brand').click()

print(app)
with open('gamesdata.txt', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=game_info)
    writer.writeheader()
    writer.writerows(app)

# most_players_now = most_played.find_elements(By.CSS_SELECTOR, '.app .text-center green')
# m_players = [player.text for player in most_players_now[1: ]]
# print(m_players)
# peak_today = most_played.find_elements(By.CLASS_NAME, 'text center')
# p_today = [peak for peak in peak_today[1: ]]
# print(m_games, len(m_games), m_players, len(m_games), p_today, len(p_today))
# df = pd.DataFrame({'Most_played': m_games,
#                    'Players Now': m_players,
#                    'Peak Today': p_today})
# print(df)

# trending = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[1]/div[2]')
# trending_games = trending.find_elements(By.CLASS_NAME, 'css-truncate')
# t_games = [game.text for game in trending_games]
# print(t_games)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Set up Chrome options
chrome_options = Options()
"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode, i.e., without a GUI
"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""

chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Set path to chromedriver as per your configuration
webdriver_service = Service(r'C:\Users\thema\OneDrive\Documents\chromedriver_win32\chromedriver.exe')


# Choose the appropriate WebDriver for your browser. Here, we use Chrome.
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

class Card:
    all_instance = []
    
    def __init__(self, name, img, num, set):
        self.name = name
        self.img = img
        self.num = num
        self.set = set
        Card.all_instance.append(self)
    
    @classmethod    
    def get_all_instance(self):
        return self.all_instance

# Load the webpage
url = f"https://jp.pokellector.com/sets"
driver.get(url)
# Wait for the page to fully render
driver.implicitly_wait(4)  # Adjust the wait time as needed
driver.maximize_window()

series_tab = driver.find_elements(By.CLASS_NAME, 'buttonlisting')
for series in series_tab:
    set_buttons = series.find_elements(By.CLASS_NAME, 'button')
    for button in set_buttons:
        url = button.get_attribute('href')
        driver.execute_script("window.open(arguments[0], '_blank')", url)
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        

        page = requests.get(url)
        content = page.content
        
        soup = BeautifulSoup(content, 'html.parser')
        
        card_arr = soup.find_all('div', class_ = 'card')
        for i, card in enumerate(card_arr):
            link = 'https://jp.pokellector.com' + str(card.find('a').get('href'))
            page2 = requests.get(link)
            content2 = page2.content
            soup2 = BeautifulSoup(content2, 'html.parser')
            
            infoblurb = soup2.find('div', class_ = 'infoblurb')
            if infoblurb is not None:
                rows = infoblurb.find_all('div')
                card_info = []
                for i, row in enumerate(rows):
                    if 'JPN' in row.find('strong').text and row.find('strong').text is not None:
                        name = row.find('a').text
                        card_info.append(name)
                    else:
                        card_info.append(None)
                no_row = rows[-1]
                card_no = no_row.find('a').text
                
                set_row = rows[-2]
                set = set_row.find('a').text
                
                img_sec = soup2.find('div', class_ = 'card')
                img = img_sec.find('img').get('src')
                
                Card(card_info[0], img, card_no, set)
        print('Set completed')    
        
        driver.close()
        driver.switch_to.window(window_handles[0])
        
        
dic = []

all_cards = Card.get_all_instance()

for card in all_cards:
    dic.append({
        "Name" : card.name,
        "Image" : card.img,
        "Number" : card.num, 
        "Set" : card.set
    })
    
dataframe = pd.DataFrame(dic)
dataframe = dataframe.sort_values(by = ['Set', 'Number'])
dataframe.to_excel("pcj_data2.xlsx", index = False)
        

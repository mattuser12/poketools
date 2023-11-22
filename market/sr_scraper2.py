from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd

# Set up Chrome options
chrome_options = Options()
"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode, i.e., without a GUI
"""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""

# Set path to chromedriver as per your configuration
webdriver_service = Service(r'C:\Users\thema\OneDrive\Documents\chromedriver_win32\chromedriver.exe')

# Choose the appropriate WebDriver for your browser. Here, we use Chrome.
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Load the webpage
def switch_page(i):
    url = f"https://www.pokemon-card.com/card-search/index.php?keyword=&se_ta=&regulation_sidebar_form=all&pg=&sc_rare_sr=1&illust=&sm_and_keyword=true&page={i}"
    driver.get(url)
    # Wait for the page to fully render
    driver.implicitly_wait(20)  # Adjust the wait time as needed
    driver.maximize_window()


# Find the card data elements
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
    

switch_page(1)
pages = driver.find_element(By.CLASS_NAME, "AllNum")
pages_num = int(pages.text)


for j in range(1, pages_num + 1):
    switch_page(j)
    card_elements = driver.find_elements(By.CLASS_NAME, "List_item")
    card_elements = card_elements[:-1]
    print(f'Now on page {j}')
    for i, card_element in enumerate(card_elements):
        #img_el = card_element.find_element(By.TAG_NAME, 'img')
            
        card_element.click()
        
        # switch main window to popup window
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        driver.implicitly_wait(5)
        driver.maximize_window()

        # MAIN SECTION
        card_main_section = driver.find_element(By.CLASS_NAME, 'Section')

        card_name = driver.find_element(By.TAG_NAME, 'h1')
        card_name = card_name.text
        
        card_img = card_main_section.find_element(By.TAG_NAME, 'img')
        card_img = card_img.get_attribute('src')

        card_num = card_main_section.find_element(By.CLASS_NAME, 'subtext')
        card_num = card_num.text
        
        
        # SUB SECTION
        card_sub_section = driver.find_element(By.CLASS_NAME, 'SubSection')
        card_sub_section2 = card_sub_section.find_element(By.CLASS_NAME, 'List_item')
        card_set_name = card_sub_section2.text
        card_set_id = card_sub_section2.find_element(By.TAG_NAME, 'a')
        # card_set_id = card_sub_section2.get_attribute('href')
        

        text = card_set_id.text
        pattern = r'「(.*?)」'

        match = re.search(pattern, text)
        if match:
            value = match.group(1)
            card_set_id = value
        
        Card(card_name, card_img, card_num, card_set_id)

            
        driver.close()
        driver.switch_to.window(window_handles[0])
        
        if (i+1)%5 == 0:
            driver.implicitly_wait(1)
            scroll_amount = (i+1)*23  # Adjust the scroll amount as needed
            driver.execute_script("window.scrollBy(0, {0})".format(scroll_amount))
    
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
dataframe.to_excel("pcj_data.xlsx", index = False)

# Quit the browser
# driver.quit()
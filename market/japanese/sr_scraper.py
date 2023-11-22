import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

def sr_searcher():
    links = [0]*20
    for i in range(len(links)):
        links[i] = f'https://www.pokemon-card.com/card-search/index.php?keyword=&se_ta=&regulation_sidebar_form=all&pg=&sc_rare_sr=1&illust=&sm_and_keyword=true&page={i+1}'
    
    for i in range(len(links)):
        page = requests.get(links[i])
        content = page.content
        
        soup = BeautifulSoup(content, 'html.parser')
        arr = soup.find('section', class_ = 'Section')
        
        cards = arr.find_all('li', class_ = 'List_item')
        for j in range(len(cards)):
            print(cards[j])
            return
        

    
sr_searcher()
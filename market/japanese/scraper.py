import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

set_links = {
    'scarlet': 'https://jp.pokellector.com/Scarlet-ex-Expansion/', 
}

def card_scraper(set_links):
    for link in set_links:
        url = set_links[link]
        page = requests.get(url)
        content = page.content
        
        soup = BeautifulSoup(content, 'html.parser')
        cards = soup.find_all('div', class_='card')
        card_link = [0]*len(cards)
        for i in range(len(cards)):
            card_link[i] = 'https://jp.pokellector.com/' + cards[i].find('a').get('href')
        
        # Extracting total cards in set (excluding SRs) from first card
        first_card_page = requests.get(card_link[0])
        first_page_cont = first_card_page.content
        first_soup = BeautifulSoup(first_page_cont, 'html.parser')
        first_info = first_soup.find('div', class_ = 'infoblurb')
        first_infoblurb = first_info.find_all('a')
        cards_in_set = first_infoblurb[-1].string
        tot_cards = cards_in_set.split('/')
        tot_cards = tot_cards[1]
        
        tot_cards_sr_inc = len(card_link)
        card_link = card_link[int(tot_cards):-1]
        
        print(card_link)
            
        
card_scraper(set_links)
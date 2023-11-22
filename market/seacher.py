import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import os
import glob

"""def start():
    os.chdir('O:\Folder\code\set data')
    
    files = glob.glob('*.xslx')
    for file in files:
        global card_data
        df = pd.read_excel(files)
        excess_cards = len(df) - df['Cards in set'][0]
        if excess_cards != 0:
            df = df.tail(excess_cards)
        card_data = df.to_dict('records')
        return"""


df = pd.read_excel('sets_data.xlsx')
excess_cards = len(df) - df['Cards in set'][0]
if excess_cards != 0:
    df = df.tail(excess_cards)


# card_data = df.set_index('Name').T.to_dict('dict')
card_data = df.to_dict('records')

done_cards = []


class Card:
    def __init__(self, pokemon, v, set, num):
        self.pokemon = pokemon
        self.v = v
        self.set = set
        self.num = num

ebay_all_listing = []
temp2 = []

"""
def listing_add_active(url):
    page = requests.get(str(url))
    content = page.content
    
    soup = BeautifulSoup(content, 'html.parser')
    
    listing = {}

    listing['Title'] = soup.find('h1', class_ = 'x-item-title__mainTitle').span.text
    listing['Price'] = soup.find('span', attrs = {'itemprop': 'price'}).span.text


    about_section = soup.find('div', class_ = 'ux-layout-section__item ux-layout-section__item--table-view')
    about_section_rows = about_section.find_all('div', class_ = 'ux-layout-section__row')
    test = about_section_rows[1].find('div', class_ = 'ux-labels-values__labels')

    about_section_labs = [0]*len(about_section_rows)*2
    about_section_vals = [0]*len(about_section_rows)*2

    for i in range(len(about_section_rows)-1):
        labs = about_section_rows[i].find_all('div', class_ = 'ux-labels-values__labels')
        vals = about_section_rows[i].find_all('div', class_ = 'ux-labels-values__values-content')
        for j in range(2):
            about_section_labs[j + i*2] = labs[j].text
            about_section_vals[j + i*2] = vals[j].text
            listing[about_section_labs[j + i*2]] = about_section_vals[j + i*2]

    ebay_all_listing.append(listing)"""


def listing_add_sold(url, query, pokemon, set, num, cardnum, j):
    # print(url)
    page = requests.get(str(url))
    content = page.content
    
    soup = BeautifulSoup(content, 'html.parser')
    
    listing = {}
    listing['Number'] = num
    listing['Query'] = query
    listing['Pokemon'] = pokemon
    listing['Set'] = set
    

    title = soup.find('h1', id = 'itemTitle')
    if title is not None and str(cardnum) in title.text:
        if 'Details about' in str(title.text): 
            listing['Title'] = title.text.replace('Details about','').strip()
        else:
            listing['Title'] = title.text
    else:
        return
    
    outright = soup.find('div', class_ = 'u-flL w29 vi-price')
    auction = soup.find('div', class_ = 'u-flL w29 vi-price-np')
    
    cost = r'\d+\.\d{2}'
    currency = r'[A-Z]{2,3}'
    
    if outright is not None:
        costmatch = re.search(cost, outright.text.strip())
        currencymatch = re.search(currency, outright.text.strip())
        if costmatch and currencymatch:
            listing['Price'] = float(costmatch.group())
            listing['Currency'] = currencymatch.group()
        #listing['Price'] = outright.text.strip()
    elif auction is not None:
        costmatch = re.search(cost, auction.text.strip())
        currencymatch = re.search(currency, auction.text.strip())
        if costmatch and currencymatch:
            listing['Price'] = float(costmatch.group())
            listing['Currency'] = currencymatch.group()
        #listing['Price'] = auction.text.strip()


    bar = soup.find('div', id = 'mainContent')
    datebar = bar.find('span', id = 'bb_tlft')

    if datebar is not None:
        date = datebar.text.strip()
        date = date[0:12]
        dateobj = datetime.strptime(date, '%d %b, %Y')
        listing['Date Sold'] = dateobj.strftime('%d/%m/%Y')


    about_section = soup.find('div', class_ = 'vim x-about-this-item')
    if about_section is not None:
        about_section_rows = about_section.find_all('div', class_ = 'ux-layout-section__row')
        # print(len(about_section_rows))
        # test = about_section_rows[1].find('div', class_ = 'ux-labels-values__labels')

        about_section_labs = [0]*len(about_section_rows)*2
        about_section_vals = [0]*len(about_section_rows)*2

        for i in range(len(about_section_rows)-1):
            labs = about_section_rows[i].find_all('div', class_ = 'ux-labels-values__labels')
            vals = about_section_rows[i].find_all('div', class_ = 'ux-labels-values__values')
            for j in range(2):
                if about_section_labs[j] and about_section_vals[j] is not None:
                    about_section_labs[j + i*2] = labs[j].text
                    # print(labs[j].text)
                    about_section_vals[j + i*2] = vals[j].text
                    #print(vals[j].text)
                    listing[about_section_labs[j + i*2]] = about_section_vals[j + i*2]
                    
    listing['URL'] = url
    temp2.append(listing)
    
    
    # ebay_all_listing.append(listing)


    
"""    
def listing_view(dict):
    for i in range(len(dict)):
        for key, value in dict[i].items():
            print(f'{key}: {value}') 
"""


def listing_search(pokemon, set, num, cardnum, j):
    # Search for multiple sold listings of singular pokemon
    query = f'Pokemon TCG {pokemon} {set} {num}'
    query = query.replace(' ', '+')
    url = f"https://www.ebay.com.au/sch/i.html?_nkw={query}&_sacat=0&LH_Complete=1&LH_Sold=1"
    page = requests.get(url)
    content = page.content
    
    dict = {}
    
    soup = BeautifulSoup(content, 'html.parser')
    
    listings = soup.find('div', class_ = 'srp-river-results clearfix', id = 'srp-river-results')
    url_list = listings.find_all('li', class_ = 's-item s-item__pl-on-bottom')
    url_list_link = [0]*len(url_list)
    card_data_list = [0]*len(url_list)
    for i in range(len(url_list)):
        temp = url_list[i].find('a', class_ = 's-item__link')
        url_list_link[i] = temp.get('href')
    if len(url_list_link) <= 5:
        return
    for i in range(len(url_list_link)):
        # Every sold listing link for singular pokemon
        listing_add_sold(url_list_link[i], query, pokemon, set, num, cardnum, j)
        # print(card_dict[j])
    
    df = pd.DataFrame.from_dict(temp2)
    # df = df.sort_values(by = 'Date Sold')
    
    with pd.ExcelWriter(f'Price Data {set}.xlsx') as writer:
        df.to_excel(writer, index=False)
    
    print(f'{cardnum}/{len(card_data)} found.')
    
    done_cards.append(card_data[j])
    cardf = pd.DataFrame.from_dict(done_cards)
    with pd.ExcelWriter(f'Done Cards.xlsx') as writer:
        df.to_excel(writer, index=False)
        
    return
    
    


# listing_add('https://www.ebay.com.au/itm/185858161226?_trkparms=amclksrc%3DITM%26aid%3D1110006%26algo%3DHOMESPLICE.SIM%26ao%3D1%26asc%3D247311%26meid%3D3b23bac2dc994b388cdd9adaf9610638%26pid%3D101195%26rk%3D3%26rkt%3D12%26sd%3D385410043339%26itm%3D185858161226%26pmt%3D1%26noa%3D0%26pg%3D2047675%26algv%3DSimplAMLv11WebTrimmedV3MskuWithLambda85KnnRecallV1V4V6ItemNrtInQueryAndCassiniVisualRankerAndBertRecallCPCBlended&_trksid=p2047675.c101195.m1851&amdata=cksum%3A1858581612263b23bac2dc994b388cdd9adaf9610638%7Cenc%3AAQAIAAABUClE7Rni7LPdZba0E4PpnN9sqdNIfzrngjJmhUj%252BPVGabI8X4okIddREUp4Q0zc2AzeQ%252BYWQSxoBqGa9J%252Bx35NrBHVFYUVGsflNyHmFJfvouFhcLtSal3PrT8uqN34xP8tTkRtMZH%252Bjfqn4MA7rMqmrUqs%252FWYsN%252B8BlfB6NUKOEGuKnbeTP99RROlQHyQ8tBSLV%252B3Ssg95WbySCcI7Ni44%252B%252FDBY4qYTjhyTCRd%252B6D5vaZHzQlT2%252Fpw9Ku8M3nD0OnmH66M3iFNj79r8d1N5pjjzgQBjkXUFW8v3F%252FmQEUnnHmn%252FOpCImy8xCU3UFALBbrEB9iGDiTT7xRgEZPhn6AgbZjKs3IbCRx5fiyumOXFfxrTwowd6VYMdDQ7t7rIbr0iobZERDmRjubTCGJDIQhIrz8nCT8%252BZTC%252Facqn%252BZAFfW%252Fmx41ID9v5kIRbAi4yfnig%253D%253D%7Campid%3APLX_CLK%7Cclp%3A2047675')
# listing_view(ebay_all_listing[0])

"""listing_search('umbreon','vmax','evolving skies','095/203')

df = pd.DataFrame(ebay_all_listing)
writer = pd.ExcelWriter('poke_data.xlsx', engine = 'xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index = False)

writer.save()
"""

for i in range(len(card_data)):
    name = card_data[i]['Card Name']
    set_name = card_data[i]['Set']
    no = card_data[i]['Card No. as listed']
    cardnum = card_data[i]['Card No.']
    listing_search(name, set_name, no, cardnum, i)
    
    # last_key = list(ebay_all_listing.keys())[-1]
    # last_dict = ebay_all_listing[last_key]
    # print(last_dict)
    # print(card_dict[i])
    # print(f'Card {i} added to dictionary.')

"""df = pd.DataFrame(ebay_all_listing)
writer = pd.ExcelWriter('poke_data.xlsx', engine = 'xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index = False)

writer.save()

# Loop through the list of dictionaries and create a new Excel sheet for each one
for i, dictionary in enumerate(ebay_all_listing):
    # Create a new Pandas DataFrame from the current dictionary
    df = pd.DataFrame.from_dict(dictionary, orient='index').transpose()
    # Write the DataFrame to a new Excel file with a sheet name based on the current index
    with pd.ExcelWriter(f'poke_data_{i}.xlsx') as writer:
        df.to_excel(writer, sheet_name=f'Sheet{i+1}')
    print(f'Sheet {i} written')"""

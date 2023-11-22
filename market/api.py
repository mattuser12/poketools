import requests
import pandas as pd
import os

os.chdir('O:\Folder\code\set data')

headers = {'X-Api-Key': '374ed794-76c2-4c98-ae23-ceef0d38a28a'}


set_req = requests.get('https://api.pokemontcg.io/v2/sets', headers=headers)
sets = set_req.json()['data']

for i in range(len(sets)):
    id = sets[i]['id']
    params = {'q': f'set.id:{id}'}
    card_req = requests.get('https://api.pokemontcg.io/v2/cards', headers=headers, params=params)
    cards = card_req.json()['data']
    card_data = {}
    for i in range(len(cards)):
        card_data[i] = {}
        card_data[i]['Card ID'] = cards[i]['id']
        card_data[i]['Card Name'] = cards[i]['name']
        card_data[i]['Card No.'] = cards[i]['number']
        card_data[i]['Cards in set'] = 198
        card_data[i]['Card No. as listed'] = str(card_data[i]['Card No.']) + '/' + str(card_data[i]['Cards in set'])
        card_data[i]['Set ID'] = cards[i]['set']['id']
        card_data[i]['Set'] = cards[i]['set']['name']


    set_data = pd.DataFrame.from_dict(card_data)
    set_data = set_data.transpose()
    writer = pd.ExcelWriter(f'set_{id}_data.xlsx', engine = 'xlsxwriter')
    set_data.to_excel(writer, sheet_name='Sheet1', index = False)

    writer.save() 
    
    print(f'Set {id} completed.')
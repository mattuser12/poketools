card_link = [0]*len(cards)
        for i in range(len(cards)):
            card_link[i] = cards.find('a').get('href')
            print(card_link[i])
import bs4 as bs
import requests
sauce1 = []
sauce2 = []
source = requests.get('https://store.steampowered.com/explore/new/').text
soup = bs.BeautifulSoup(source, 'lxml')
for sauces in soup.find_all('div', class_="tab_content"):
    for sauce in sauces.find_all('div', class_="discount_final_price"):
        new = str(sauce).split(">")
        new1 = new[1].split("<")
        if new1[0] in sauce1 and new1[0] != 'Free' or 'Free To Play':
            pass
        if new1[0] == 'Free To Play':
            sauce1.append('Free')
        else:
            sauce1.append(new1[0])
    for sauce in sauces.find_all('div', class_="tab_item_name"):
        new = str(sauce).split(">")
        new1 = new[1].split("<")
        sauce2.append(new1[0])
for game, price in zip(sauce2, sauce1):
    print(game + price)
i = input('>')

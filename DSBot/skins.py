import requests

def get_prices():
    skins_data = requests.get('http://csgobackpack.net/api/GetItemsList/')

    print(skins_data.json())
    #print(skins_data.json()['items_list']['AUG | Fleet Flock (Well-Worn)'])  #'AWP | Chromatic Aberration (Battle-Scarred)'

get_prices()


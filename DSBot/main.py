import discord
from discord.ext import commands
import requests
import json

token = 'MTA0NjE5MDM5NDIxMzQwMDYzNw.GHaD9k.CvAEyn9nTildSZp5FHM0hhm0Ayv6_2lgP_eF48'
bot = commands.Bot(intents = discord.Intents.all(), command_prefix='-')

def create_embed_skin_data(skinn):
    data = get_item_list()

    keys = list(filter(lambda x: skinn in x, list(data.keys())))

    skins_d = sort_sost(list(filter(lambda x: "StatTrak" not in x and 'Souvenir' not in x, keys)))
    skins_d_ST = sort_sost(list(filter(lambda x: "StatTrak" in x or "Souvenir" in x, keys)))

    skin_image_url = 'https://community.akamai.steamstatic.com/economy/image/' + data[skins_d[0]]["icon_url"]

    embed = discord.Embed(title=skinn)
    embed.set_image(url=skin_image_url)

    for i in skins_d:
        sost = i[i.find('(') + 1:-1]
        try:
            ind = list(data[i]['price'].keys())[0]
            USD = str(data[i]['price'][ind]['average'])
            RUB = to_rub(USD)
        except:
            USD = "None"
            RUB = "None"
        embed.add_field(name=f'{sost}', value=f'{USD}$ {RUB}₽', inline=False)

    for i in skins_d_ST:
        sost = i[i.find('(') + 1:-1]
        ST = i.split()[0]
        try:
            ind = list(data[i]['price'].keys())[0]
            USD = str(data[i]['price'][ind]['average'])
            RUB = to_rub(USD)
        except:
            USD = "None"
            RUB = "None"
        embed.add_field(name=f'{ST} {sost}', value=f'{USD}$ {RUB}₽', inline=False)  
    return embed

exteriors = ['factory', 'new', 'well', 'worn', 'field', 'tested', 'minimal', 'wear', 'battle', 'scarred']

def sort_sost(a):
    out = [''] * 5
    for i in a:
        if 'Factory New' in i:
            out[0] = i
        if 'Minimal Wear' in i:
            out[1] = i
        if 'Well-Worn' in i:
            out[2] = i
        if 'Field-Tested' in i:
            out[3] = i
        if 'Battle-Scarred' in i:
            out[4] = i
    out = list(filter(lambda x: x != '', out))
    return out

def get_item_list():

    url = 'http://csgobackpack.net/api/GetItemsList/v2/'
    
    skin_data = requests.get(url).json()

    with open('skins_all.json', 'w') as file:
        json.dump(skin_data, file, indent=4)
    file.close()

    with open('skins_all.json', 'r') as file:
        data = json.load(file)
    file.close()

    return data['items_list']

def to_rub(a):
    data_valuti = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    return str(round(float(a) * float(data_valuti['Valute']['USD']['Value']), 2))

@bot.event
async def on_ready():
    print("Бот запущен!")

@bot.command(name='-help')
async def help(ctx):
    await ctx.send("Напиши -skin 'Оружие' 'Название скина' (Все на английском")

@bot.command(name='skin')
async def skin(ctx, gun="", skin_name1='', skin_name2=''):
    
    if skin_name2 == '':
        skinn = f'{gun.upper()} | {skin_name1.capitalize()}'
    else:
        skinn = f'{gun.upper()} | {skin_name1.capitalize()} {skin_name2.capitalize()}'
    
    embed = create_embed_skin_data(skinn)
    
    await ctx.send(embed=embed)
    

@bot.command(name='knife')
async def knife(ctx, type='', skin_name1='', skin_name2=''):
    knifes = ['butterfly', 'flip', 'falchion', 'ursus']
    if type.lower() == 'm9':
        if skin_name2=='':
            skinn = f'{type.upper()} Bayonet | {skin_name1.capitalize()}'

        elif skin_name1 == '' and skin_name2 == '':
            skinn = f'{type.upper()} Bayonet'

        else:
            skinn = f'{type.upper()} Bayonet | {skin_name1.capitalize()} {skin_name2.capitalize()}'

    elif type.lower() in knifes:
        if skin_name2=='':
            skinn = f'{type.capitalize()} Knife | {skin_name1.capitalize()}'

        elif skin_name1 == '' and skin_name2 == '':
            skinn = f'{type.capitalize()} Knife'

        else:
            skinn = f'{type.capitalize()} Knife | {skin_name1.capitalize()} {skin_name2.capitalize()}'
    else:
        if skin_name2=='':
            skinn = f'{type.capitalize()} | {skin_name1.capitalize()}'

        elif skin_name1 == '' and skin_name2 == '':
            skinn = f'{type.capitalize()}' 

        else:
            skinn = f'{type.capitalize()} | {skin_name1.capitalize()} {skin_name2.capitalize()}'
    
    embed = create_embed_skin_data(skinn)
    
    await ctx.send(embed=embed)

bot.run(token)
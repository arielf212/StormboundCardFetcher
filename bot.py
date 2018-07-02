import csv
import difflib
import os
from discord.ext import commands

# made by FireofGods

bot = commands.Bot(command_prefix='?') # bot creation

def get_card_name(text):
    '''takes a string and extracts card names from it. card names are encapsulated in [[xxxx]] where xxxx is the card name'''
    cards = [] # list of names of cards
    start = text.find('[[')
    while start != -1: # until there are no more brackets
        end = text.find(']]')
        if end == -1:
            return cards # if there is an opener but no closer then someone fucked up
        else:
            cards.append(text[start+2:end]) # gets the name of the card
        text = text[end+2 : ] # cuts out the part with the card
        start = text.find('[[') # and the circle begins anew
    return cards

def load_cards():
    cards = {}
    with open('card_list' , 'r') as fcard_list:
        card_list = csv.reader(fcard_list , delimiter = '%')
        for row in card_list:
            name , link = row
            cards[name] = link
    return cards

@bot.event
async def on_message(message):
    #variables
    honor_cards = {'conflictor': 'Conflicted drakes' , 'frozenearth' : 'broken earth' ,'gale' : 'green gale' ,'wander' : 'wandering wyrms' ,
                   'omer' : 'draconic roamer' , 'dan su' : 'dangerous suitors' , 'spare' : 'spare dragonlings' , 'ludo': 'ludic matriarch'}

    #the function
    if message.content.find('[[') != -1:
        cards = get_card_name(message.content) # get the card name out of the message
        for card in cards:
            if difflib.get_close_matches(card , honor_cards , n=1 , cutoff=0.5):
                card = honor_cards[difflib.get_close_matches(card , honor_cards , n=1 , cutoff=0.5)[0]]
                await bot.send_message(message.channel , card_list[difflib.get_close_matches(card , card_list ,  n = 1 , cutoff=0.5)[0]])
            else:
                await bot.send_message(message.channel , card_list[difflib.get_close_matches(card , card_list , n = 1)[0]])

#main
card_list = load_cards()
print("done loading cards!")
bot.run(os.environ.get('BOT_TOKEN'))
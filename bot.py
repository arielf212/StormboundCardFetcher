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
    if message.content.find('[[') != -1:
        cards = get_card_name(message.content) # get the card name out of the message
        for card in cards:
            await bot.send_message(message.channel , card_list[difflib.get_close_matches(card , card_list , n = 1)[0]])

#main
card_list = load_cards()
bot.run(os.environ.get('BOT_TOKEN')

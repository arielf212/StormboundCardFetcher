import csv
from fuzzywuzzy import fuzz
import difflib
import os
from discord.ext import commands

# made by FireofGods

bot = commands.Bot(command_prefix='?') # bot creation
card_list = []
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

def get_link(card):
    max_ratio = (' ', 0)  # maximum score in ratio exam
    max_partial = (' ', 0)  # maximum sort in partial ratio exam
    for entry in card_list:
        # lets check if an entry is "good enough" to be our card
        ratio = fuzz.ratio(card, entry)
        partial = fuzz.partial_ratio(card, entry)
        if ratio > max_ratio[1]:
            max_ratio = (entry, ratio)
            list_ratio = [max_ratio]
        elif ratio == max_ratio[1]:
            list_ratio.append((entry, ratio))
        if partial > max_partial[1]:
            max_partial = (entry, partial)
            list_partial = [max_partial]
        elif partial == max_partial[1]:
            list_partial.append((entry, partial))
    if max_partial[1] > max_ratio[1]:
        return card_list[max_partial[0]]
    return card_list[max_ratio[0]]

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
    honor_cards = {'conflictor': 'conflicted drakes' , 'frozenearth' : 'broken earth drakes' ,'gale' : 'greengale serpents' ,'wander' : 'wandering wyrms' ,
                   'omer' : 'draconic roamers' , 'dan su' : 'dangerous suitors' , 'spare' : 'spare dragonlings' , 'ludo': 'ludic matriarch' ,
                   'q.q' : 'archdruid earyn' , 'youngestmammal1' : 'finite loopers'}
    # note: q.q's card isnt really his card, but I still gave it to him

    #the function
    if message.content.find('[[') != -1:
        cards = get_card_name(message.content) # get the card name out of the message
        for card in cards:
            if difflib.get_close_matches(card , honor_cards , n=1 , cutoff=0.65):
                # check if a card name is actually a honored person's name. if it is then get his card.
                card = honor_cards[difflib.get_close_matches(card , honor_cards , n=1 , cutoff=0.65)[0]]
                await bot.send_message(message.channel , card_list[difflib.get_close_matches(card , card_list,  n = 1 , cutoff=0.65)[0]])
            else:
                card = get_link(card)
                await bot.send_message(message.channel , card)
    elif message.content.startswith('!'):
        #special commands
        parameters = message.content.split(' ')
        if parameters[0] == '!alive':
            await bot.send_message(message.channel , 'im alive and well!')
        if parameters[0] == '!linkme':
            cards = ' '.join(parameters[1: ]).split(',')
            for card in cards:
                if difflib.get_close_matches(card, honor_cards, n=1, cutoff=0.65):
                    # check if a card name is actually a honored person's name. if it is then get his card.
                    card = honor_cards[difflib.get_close_matches(card, honor_cards, n=1, cutoff=0.65)[0]]
                    await bot.send_message(message.channel,
                                           card_list[difflib.get_close_matches(card, card_list, n=1, cutoff=0.65)[0]])
                else:
                    card = get_link(card)
                    await bot.send_message(message.channel, card)

#main
card_list = load_cards()
print("done loading cards!")
bot.run('NDYzMDk1MjAzMzY1MTI2MTU0.Dhre2A.Q9kY09phR10E6nTr1T0o47foDjY')
import os

import random
import json

import discord

client = discord.Client()

def draw():
  # If deck is empty return None to avoid
  # syntax error of drawing from an empty list
  global deck
  if not deck:
    return None
  
  card = random.choice(deck)
  deck.remove(card)
  return card

def shuffle():
  # Reset the deck to the list of cards
  global deck
  deck = cards.copy()
  print(deck)


@client.event
async def on_ready():
  with open("tarot-cards/tarot-images.json") as file:
    raw_cards = file.read()

  global cards
  cards = json.loads(raw_cards)["cards"]
  global deck
  deck = cards.copy()

  global card_images
  card_images = {card_img: discord.File("tarot-cards/cards/" + card_img, filename=card_img) for card_img in os.listdir("tarot-cards/cards")}
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  # Return if the messsage is from the bot
  if message.author == client.user:
    return

  if message.content.startswith('!draw'):
    card = draw()

    if not card:
      await message.channel.send("No more cards remaining, please shuffle the deck using !shuffle.")
      return

    global card_images
    file = card_images[card["img"]]
    embed = discord.Embed()
    img_url = "attachment://" + card["img"]
    embed.set_image(url = img_url)

    await message.channel.send(content=card["name"],file=file, embed=embed)

  elif message.content.startswith('!shuffle'):
    shuffle()
    await message.channel.send("Deck has been shuffled!")


client.run(os.environ['BOT_TOKEN'])
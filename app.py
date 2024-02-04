#!/usr/bin/env python3

from dalle3 import generate_image

import os, io
from nextcord import Intents, utils, File
from nextcord.ext import commands
import requests

with open('/mnt/secrets/discord_bot_token.txt', 'r') as file:
    discord_bot_token = file.read().strip()

with open('/mnt/secrets/openai_api_key.txt', 'r') as file:
    openai_api_key = file.read().strip()

os.environ['DISCORD_BOT_TOKEN'] = discord_bot_token
os.environ['OPENAI_API_KEY'] = openai_api_key

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def send_image_to_pixoo(image, x, y, push):
    url = 'http://192.168.42.247:5000/image'
    image_data = image.getvalue()
    files = {
        'image': ('image.png', image_data, 'image/png') 
    }

    data = {
        'x': x,
        'y': y,
        'push_immediately': push
    }

    response = requests.post(url, files=files, data=data)

    # Check response
    print(response.status_code)
    print(response.text)

# # Usage
# image = open('image.png', 'rb').read() 
# send_image(image, 0, 0, True)

# !hi
# Hello!
@bot.command(name='hi')
async def SendMessage(ctx):
    # Replace 'RoleName' with the name of the role you want to check for
    role = utils.get(ctx.guild.roles, name="openai")
    if role in ctx.author.roles:
        await ctx.send('Hello!')
    else:
        await ctx.send('Sorry, you do not have the required role to use this command.')

@bot.command(name='dalle-3')
async def SendMessage(ctx, *, prompt_text: str):
    role = utils.get(ctx.guild.roles, name="openai")
    pixoo_role = utils.get(ctx.guild.roles, name="pixoo")
    if role in ctx.author.roles:
        try:
            # Pass the prompt_text to your function here
            image_bytes = generate_image(prompt_text)
            image_file = File(image_bytes, filename='image.png')
            await ctx.send(file=image_file)
            if pixoo_role in ctx.author.roles and "pixelart" in prompt_text.lower():
                try:
                    # Send the image to Pixoo
                    send_image_to_pixoo(image_bytes, 0, 0, True)
                except Exception as e:
                    # Send the error message to the Discord chat
                    await ctx.send(f'An error occurred while sending the image to Pixoo: {str(e)}')

        except Exception as e:
            # Send the error message to the Discord chat
            await ctx.send(f'An error occurred while generating the image: {str(e)}')
    else:
        await ctx.send('Sorry, you do not have the required role to use this command.')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
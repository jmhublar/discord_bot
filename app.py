#!/usr/bin/env python3

from dalle3 import generate_image

import os
from nextcord import Intents, utils, File
from nextcord.ext import commands

with open('/mnt/secrets/discord_bot_token.txt', 'r') as file:
    discord_bot_token = file.read().strip()

with open('/mnt/secrets/openai_api_key.txt', 'r') as file:
    openai_api_key = file.read().strip()

os.environ['DISCORD_BOT_TOKEN'] = discord_bot_token
os.environ['OPENAI_API_KEY'] = openai_api_key

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

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
    if role in ctx.author.roles:
        try:
            # Pass the prompt_text to your function here
            image_bytes = generate_image(prompt_text)
            image_file = File(image_bytes, filename='image.png')
            await ctx.send(file=image_file)
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
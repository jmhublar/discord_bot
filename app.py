#!/usr/bin/env python3

#!/usr/bin/env python3
import os
from nextcord import Intents, utils
from nextcord.ext import commands

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

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
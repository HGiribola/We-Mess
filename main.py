import discord
from discord.ext import commands

from dependences import send

from secrets import token

prefix = '/'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)

# collect discord server data


@bot.event
async def on_ready():
    print(f' Bot {bot.user.name} está online')


send.setup(bot)

bot.run(token)

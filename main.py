import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument

import config.data as config

# prefix and token
prefix = config.get_config('prefix')
token = open(config.get_config('token')).readline()

# bot status
status = config.get_string('status')

# bot prefix
bot = commands.Bot(command_prefix=prefix)

# logging the starting of the bot into the console
@bot.event
async def on_ready():
  # set active status
  if status != '':
    await bot.change_presence(activity=discord.Game(status))


  # remove default help command
  print("\n# logged in as {0.user}".format(bot)+"\n")


# starting the bot
bot.run(token)
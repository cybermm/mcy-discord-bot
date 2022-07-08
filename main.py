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
  print(f"\n# logged in as {bot.user}\n")

# remove the "command not found" error from the console
@bot.event
async def on_command_error(ctx, error):
  # error to skip
  skip = [CommandNotFound, MissingRequiredArgument]

  # return if error is to skip type
  for type in skip:
    if isinstance(error, type):
      return

  raise error

# starting the bot
bot.run(token)
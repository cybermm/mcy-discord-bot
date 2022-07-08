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

# extensions
extensions = config.get_config('extensions')
disabled_extensions = config.get_config('disabled_extensions')

# loading the extensions
if __name__ == '__main__':
  # remove default help command
  bot.remove_command('help')

  # logging unloaded extensions
  if len(disabled_extensions) != 0:
    print('\nFollowing extensions are disabled:')

    for extension in disabled_extensions:
      print(f"[Disabled]\t{extension} has been disabled.")

  # logging loaded extensions
  if len(extensions) != 0:
    print("\nLoading the extensions:")

    for extension in extensions:
      try:
        bot.load_extension(extension)
        print(f"[Success]\t{extension} loaded successfully.")

      except Exception as e:
        print(f"[Error]\tAn error occurred while loading {extension}\n" + str(e) + "\n")

# logging the starting of the bot into the console
@bot.event
async def on_ready():
  # set active status
  if status != '':
    await bot.change_presence(activity=discord.Game(status))

  # remove default help command
  print(f"\n# Logged in as {bot.user}\n")

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
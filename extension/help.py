from discord.ext import commands

import config.data as config

help = config.get_string('help')

def get_msg(bot):
  """Fabricates the output message by loading extensions and commands informations."""

  msg = "```markdown\n#####\thelp center\t#####\n"

  # loop through extensions
  for extension_name in bot.cogs:
    extension = f"\n> {extension_name}\n"

    # loops all commands in extension
    commands = bot.get_cog(extension_name).get_commands()
    for command in commands:
      extension += command.name

      if not command.description == '':
        extension += f" | {command.description}"

      extension += "\n"

    msg += extension

  msg += '```'
  return msg

class help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='help', description=help["user_help"])
  async def help_user(self, ctx):
    await ctx.send(get_msg(self.bot))

def setup(bot):
  bot.add_cog(help(bot))
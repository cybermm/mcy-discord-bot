import asyncio
import functools

from discord.ext import commands
from discord.channel import DMChannel

import config.data as config

ERROR = config.get_string('commands')
BANNED = config.get_string('banned')

ROLES = config.get_config('roles')
CHANNELS = config.get_config('channels')

def check(roles='', channels='', dm_flag=None):
  """decorator to check role permissions and context for the user invoking a bot command"""

  def perm(cmd):
    """wrapper method to allow our own method to be executed before the original method"""
    @functools.wraps(cmd)
    async def wrapper(*args, **kwargs):
      """checks permissions of the message before executing command"""

      # wrapper() args is the original args passed to the command being checked
      # second element of args will always be the discord message (context object)

      ctx = args[1]

      if type(ctx) is not commands.Context:
        print("Error: Missing ctx variable in @check() call in", cmd.__name__, " command!")
        raise commands.MissingRequiredArgument(ctx)

      # 1. checking if dm_flag is set and if message is in DMs
      if dm_flag is not None:
        try:
          check_context(ctx, dm_flag)

        # errors out if the message is not in the appropriate context
        except commands.PrivateMessageOnly as e:
          await error_response(ctx, 'context_dm_only', delete_ctx=True)
          return False

        except commands.NoPrivateMessage as e:
          await error_response(ctx, 'context_public_only', delete_msg=False)
          return False

      # 2. checking for if the message is in the list of channels provided. dm_flag = False for no DM
      if channels:
        dm_allowed = dm_flag is not False

        try:
          check_channels(ctx, channels, dm_allowed)

          # errors out if channel is not in the channels whitelist
        except commands.CommandInvokeError as e:
          await error_response(ctx, 'channel_not_allowed')
          return False

      # 3. checking if the message author has a role in the list of whitelisted roles.
      if roles:
        try:
          check_roles(ctx, roles)

        except commands.MissingAnyRole as e:
          await error_response(ctx, 'no_perm')
          return False

      # 4. if all checks succeeded, then executes the original command.
      return await cmd(*args, **kwargs)

    return wrapper

  return perm

async def is_sanitized(msg, ctx=None, error_msg='not_sanitized', banned_chars=None):
  """recursively checks user input for any forbidden characters"""
  if banned_chars:
    banned = banned_chars

  else:
    banned = BANNED

  for text in msg:
    # check to see if arg is a list to also recursively sanitize anything in it
      if type(text) is tuple or \
        type(text) is list:
          await is_sanitized(ctx, text)

      else:
        # otherwise, check text for sanitation.
        has_banned_chars = [char for char in text if char in banned]

        if has_banned_chars:
          
          if ctx and error_msg:
            await error_response(ctx, error_msg)

          raise commands.BadArgument(message=msg)

  # if all text is sanitary, then return bool True
  return True

def check_context(ctx, dm_flag):
  """checks if the context is correct (DMs or public channel)"""

  dm_message = type(ctx.channel) is DMChannel

  # if message is not a DM and the command is DM only (dm_flag True)
  if not dm_message and dm_flag:
    raise commands.PrivateMessageOnly

  # if message is a DM but the command is not allowed in DMs (dm_flag False)
  elif dm_message and not dm_flag:
    raise commands.NoPrivateMessage

  return dm_message

async def error_response(ctx, error_msg, delete_msg=True, delete_ctx=False):
  """makes the bot send a response back to the ctx.channel as err_msg, and deletes the message automatically"""

  # tries to retrieve ERROR_STRING[error_msg], but if not found, then defaults to error_msg
  error_output = ERROR.get(error_msg, error_msg)

  bot_message = await ctx.send(error_output)

  if delete_msg or delete_ctx:
    await asyncio.sleep(5)

    if delete_msg:
      await bot_message.delete()

    if delete_ctx and type(ctx.channel) is not DMChannel:
      await ctx.message.delete()

def check_channels(ctx, channels, dm_allowed):
  """checks the current channel is valid for the command with arg channels"""
  if type(channels) is str:
    channels = [channels]

  # converts arg channels into corresponding channel IDs, and check if DM is ok
  valid_channels = [CHANNELS[channel] for channel in channels]
  dm_appropriate = type(ctx.channel) is DMChannel and dm_allowed

  # check if channel is in the list of channels and/or if DM is ok
  if ctx.channel.id not in valid_channels and not dm_appropriate:
    raise commands.CommandInvokeError(ctx)

  return True

def check_roles(ctx, roles):
  """checks that the user has all the required roles."""
  if type(roles) is str:
    roles = [roles]
    user = ctx.author

    # get the list of IDs from user.roles, and list of IDs from arg roles
    user_roles = [role.id for role in user.roles]
    req_roles = [ROLES[req_role] for req_role in roles]

    # check intersection of roles in user_roles and req_roles.
    if not [role for role in user_roles if role in req_roles]:
      raise commands.MissingAnyRole(roles)

    return True
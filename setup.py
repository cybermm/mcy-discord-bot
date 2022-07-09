from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='mcy-discord-bot',
   version='0.01',
   description='A bot created for usage on the Myanmar Cyber Youth discord chat server',
   license="LGPL-3.0",
   long_description=long_description,
   author=['Kyle Sin Lynn', 'Thet Paing Hein', 'Aung Myat Moe'],
   author_email='contact@cybermm.tech',
   url="http://cybermm.tech/",
   packages=['mcy-discord-bot'], 
   install_requires=['discord.py'], #external packages as dependencies

)

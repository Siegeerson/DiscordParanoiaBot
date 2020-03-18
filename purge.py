import discord, os
from discord.ext import commands
if os.path.exists("auth.txt"):
    with open("auth.txt",'r') as authF:
        auth = authF.read()

ch = 689247879487160372
client = commands.Bot(command_prefix='FC_', description='Your Friend')
@client.event
async def on_ready():
    channel = client.get_channel(ch)
    await channel.purge()
    await client.close()
    print("channel purged")

client.run(auth)

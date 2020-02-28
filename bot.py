import discord
from discord.ext import commands
client = commands.Bot(command_prefix='FC_', description='Your Friend')
auth = ""
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def close(ctx,*args):
   usr = ctx.message.author
   if usr.name == "siegeerson":
       await client.close()

@client.command()
async def cmess(ctx,*args):
    try:
        await ctx.send(input())
        
    except:
        await client.close()

#TODO: extensions/commands can be stored in seperate file
@client.command()
async def reloadC(ctx,arg):
    client.reload_extension(arg)

@client.command()
async def happiness(ctx):
    await ctx.send("`Remember, happiness is mandatory`")
    
with open("auth.txt",'r') as authF:
    auth = authF.read()
def setup(client):
    client.run(auth)
    
    print("YO")
setup()

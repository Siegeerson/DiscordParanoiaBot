import discord, os
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
        ctx = client.wait_for('message',lambda(x):x.message.user.name=="siegeerson")
        await ctx.send(ctx.message)
        
    except:
        await ctx.send("ERROR COMPUTER UNAVAILABLE")
#TODO: extensions/commands can be stored in seperate file
@client.command()
async def reloadC(ctx,arg):
    client.reload_extension(arg)

@client.command()
async def happiness(ctx):
    await ctx.send("`Remember, happiness is mandatory`")
if os.path.exists("auth.txt"):
    with open("auth.txt",'r') as authF:
        auth = authF.read()
else:
    auth =os.environ['AUTH_KEY']
    print(auth)
def setup(client):
    client.run(auth)
    
    print("YO")
setup(client)

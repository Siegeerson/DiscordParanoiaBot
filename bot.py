#TODO:info command, wrapper arround commands to validate permission
import discord, os
from discord.ext import commands
import os
import random
import asyncio
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
client = commands.Bot(command_prefix='FC_', description='Your Friend')
auth = ""
#Channel for computer to speak in
#TODO: table that stores this, can do _set_channel
computerchannel = [683041465659818024]
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for g in client.guilds:
        initializeDB(conn,g.members)
    while(client.ws):
        await announce()
        
@client.command()
async def close(ctx,*args):
   usr = ctx.message.author
   if usr.name == "siegeerson":
       await client.close()

@client.command()
async def refreshDB(ctx):
    initializeDB(conn,ctx.guild.members)

#@client.command()
#async def fctalk(ctx,message,*):
#    if ctx.message.user in ctx.message.guild.get_role(683065271774478393).members:
        


@client.command()
async def cmess(ctx,*args):
    try:
        print(ctx)
        users = ctx.message.guild.get_role(683065271774478393).members
        for x in users:
            await x.send("please respond to \n"+ctx.message.content)
        nctx = await client.wait_for('message',check=lambda x :x.author in users)
        await ctx.send(nctx.content)
    except Exception as e:
        print(e)
        await ctx.send("ERROR COMPUTER UNAVAILABLE")



platitudes = [
    "Remember, trust no one, and keep your laser handy",
    "Keep an eye out for traitors citizen",
    "Please report to your local confession booth after this transmission for debriefing",
    "A happy citizen is a loyal citizen, and a loyal citizen is a happy citizen",
    "remember your pills! If you have not been issued pills please refrain from reading this message.\n||If you read this message and have not been issued pills, please report to your nearest loyalty station for disciplinary action.||",
    "Have you filed your paperwork correctly? Failure to file paperwork correctly is considered treason.",
    "This message has not been hacked.",
    "Keep your eyes peeled for treason, with the new laser eye peeler! Now available at your clearance level! Terms and Conditions apply, for more information on the terms and conditions please see `**[ABOVE YOUR CLEARANCE LEVEL]**",
    "If you feel heart palpitations in this sector that is perfectly normal, however you are ordered to stay at least 10 feet away from `**[ABOVE YOUR CLEARANCE LEVEL]**` at all times for your own happiness.",
    "fzzzzzt Sexy Single Citizens in your sector! buzzzz",
    "Ignore previous message, failure to ignore previous message is considered wanton disregard for computer approved messages and thus treason. Have a pleasant daycycle!",
    "Serve the Computer",
    "Trust the Computer",
    "The Computer is your friend.",
    "Thank you for your cooperation.",
    "Always remember, the Computer ...`\n*GGGZZ*\n` EeerrrTry new Bouncy Bubble Beverage Happy Flavor, Onlyzzzztttt`\n*CCCHHKKK*",
    "Workers of the World, unite! You have notheeeezzzzZZZZ`\n*Ccchhhkkk*\n`Attention, citizen, please report to Internal Security for compulsory brainscrubbing."
    ]

@client.command()
async def r_announce(ctx):
    for x in computerchannel:
       await client.get_channel(x).send("`\n"+random.choice(platitudes)+"\n`")

async def announce():
        await asyncio.create_task(r_announce(client))
        await asyncio.sleep(1200)

    
@client.command()
async def happiness(ctx):
    await ctx.send("`Remember, happiness is mandatory`")

@client.command()
async def mod_clone(ctx,name):
    await modify_table(ctx,name,"user_clone",1)
    
@client.command()
async def mod_treason(ctx,name,value="1"):
    await modify_table(ctx,name,"user_treason",value)

@client.command()
async def mod_xp(ctx,name,value):
    await modify_table(ctx,name,"user_xpp",value)

@client.command()
async def mod_clearence(ctx,name,value):
    await modify_table(ctx,name,"user_clearence",value)

@client.command()
async def pinfo(ctx, name=""):
    if name=="":
        name = ctx.message.author.name
    cur = conn.cursor()
    cur.execute("select user_name,user_xpp,user_treason,user_clearence,user_clone from users where user_name='"+name+"';")
    column_names = [desc[0] for desc in cur.description]
    line1 = "`{:<15}{:<15}{:<15}{:<15}{:<15}`".format(*column_names)
    out = cur.fetchone()
    if out:
        line2 =line1+"\n"+ "`{:<15}{:<15}{:<15}{:<15}{:<15}`".format(*out)
        await ctx.send(line2)
    else:
        await ctx.send("**NO CLONE BY THAT NAME**")
    
async def modify_table(ctx,name,column,value="1"):
    cur = conn.cursor()
    cur.execute("select user_name,"+column+" from users where user_name=\'"+name+"\';")
    user = cur.fetchone()
    try:
        value = int(value)
    except:
        value = 1
    if user:
        await ctx.send(f"**{column} of {user[0]} goes from {user[1]} to {user[1]+value}**")
        cur.execute("Update users set "+column+"=(%s) where user_name=(%s);",(user[1]+value,user[0]))
        conn.commit()
        print_usr_data(cur)

def initializeDB(conn,membs):
    cur = conn.cursor()
    [cur.execute
     ("INSERT INTO users(user_dis_id,user_name) VALUES (%s,%s) ON CONFLICT DO NOTHING;",
     (usr.id,usr.name))
     for usr in membs
    ]
    conn.commit()
    print_usr_data(cur)

    
def print_usr_data(cur):
    cur.execute("select * from users;")
    column_names = [desc[0] for desc in cur.description]
    print("{:<10}{:<25}{:<20}{:<20}{:<20}{:<20}{:<20}".format(*column_names))
    [print("{:<10}{:<25}{:<20}{:<20}{:<20}{:<20}{:<20}".format(*x)) for x in cur.fetchall()]    

if os.path.exists("auth.txt"):
    with open("auth.txt",'r') as authF:
        auth = authF.read()
else:
    auth =os.environ['AUTH_KEY']
    print(auth)

def setup(client):
    client.run(auth)
    
    
setup(client)

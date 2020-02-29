import discord, os
from discord.ext import commands
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
client = commands.Bot(command_prefix='FC_', description='Your Friend')
auth = ""
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for g in client.guilds:
        initializeDB(conn,g.members)

@client.command()
async def close(ctx,*args):
   usr = ctx.message.author
   if usr.name == "siegeerson":
       await client.close()


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

#TODO: extensions/commands can be stored in seperate file
@client.command()
async def reloadC(ctx,arg):
    client.reload_extension(arg)
    
@client.command()
async def happiness(ctx):
    await ctx.send("`Remember, happiness is mandatory`")


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
    cur.execute("select user_name,user_xpp,user_treason,user_clearence from users where user_name='"+name+"';")
    column_names = [desc[0] for desc in cur.description]
    line1 = "`{:<15}{:<15}{:<15}{:<15}`".format(*column_names)
    out = cur.fetchone()
    if out:
        line2 =line1+"\n"+ "`{:<15}{:<15}{:<15}{:<15}`".format(*out)
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
    [cur.execute("INSERT INTO users(user_dis_id,user_name) VALUES (%s,%s) ON CONFLICT DO NOTHING;",
                 (usr.id,usr.name))
     for usr in membs]
    conn.commit()
    print_usr_data(cur)

    
def print_usr_data(cur):
    cur.execute("select * from users;")
    column_names = [desc[0] for desc in cur.description]
    print("{:<10}{:<25}{:<20}{:<20}{:<20}{:<20}".format(*column_names))
    [print("{:<10}{:<25}{:<20}{:<20}{:<20}{:<20}".format(*x)) for x in cur.fetchall()]
    

if os.path.exists("auth.txt"):
    with open("auth.txt",'r') as authF:
        auth = authF.read()
else:
    auth =os.environ['AUTH_KEY']
    print(auth)

def setup(client):
    client.run(auth)
    
    
setup(client)

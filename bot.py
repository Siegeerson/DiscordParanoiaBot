#TODO:info command, wrapper arround commands to validate permission --> use checks
#Todo:use better TODO structure
#Fix sql commands to correctly pass in strings using additional arguments --> arguments passed in need to be in a list
import discord, os, psycopg2,random, asyncio
from discord.ext import commands
from gtts import gTTS
from user_commands import Users
from bot_dice import Dice
from bot_mutant import Mutations
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
client = commands.Bot(command_prefix='FC_', description='Your Friend, ')
EXIT_EMOJI = '\U0000274C'
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

#remove used action cards
@client.event
async def on_reaction_add(reaction,user):
    if user!=client.user and reaction.message.embeds and reaction.message.author == client.user and reaction.emoji ==EXIT_EMOJI:
        await reaction.message.delete()
            
@client.command(hidden=True)
async def close(ctx,*args):
    usr = ctx.message.author
    if usr.name == "siegeerson":
        await client.close()

@client.command(brief="Join a voice channel")
async def join(ctx):
    try:
        voiceC = ctx.author.voice
        if voiceC:
            await voiceC.channel.connect()
    except:
        await ctx.send("Must call this command from a server")

@client.command(brief="Disconnect from a voice channel")
async def leave(ctx):
    if ctx.guild and ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()

@client.command(hidden=True)
async def say(ctx,*,message):
    if ctx.guild and ctx.guild.voice_client:
        gTTS(message).save("computer_voice.mp3")
        ctx.guild.voice_client.play(discord.FFmpegPCMAudio("computer_voice.mp3"))
        return True
    return False




@client.command(brief="talk directly to the computer")
async def cmess(ctx,*args):
    try:
        print(ctx)
        users = ctx.message.guild.get_role(683065271774478393).members
        for x in users:
            await x.send("please respond to \n"+ctx.message.content)
        nctx = await client.wait_for('message',check=lambda x :x.author in users)
        if not await say(ctx,message=nctx.content):
           await ctx.send("**"+nctx.content+"**")
    except Exception as e:
        print(e)
        await ctx.send("ERROR COMPUTER UNAVAILABLE")



platitudes = [
    "Remember, trust no one, and keep your laser handy",
    "Keep an eye out for traitors citizen",
    "Please report to your local confession booth after this transmission for debriefing",
    "A happy citizen is a loyal citizen, and a loyal citizen is a happy citizen",
    "remember your pills! If you have not been issued pills please refrain from reading this message.\n`||If you read this message and have not been issued pills, please report to your nearest loyalty station for disciplinary action.||`",
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

@client.command(brief="Send out a computer mandated announcement")
async def r_announce(ctx):
    for x in computerchannel:
        await client.get_channel(x).send("`\n"+random.choice(platitudes)+"\n`")

async def announce():
    await asyncio.create_task(r_announce(client))
    await asyncio.sleep(1200)

    
@client.command(brief="let everyone know how happy they are")
async def happiness(ctx):
    is_said = await say(ctx,message="Remember, happiness is mandatory")
    if not is_said:
        await ctx.send("`Remember, happiness is mandatory`")
        

if os.path.exists("auth.txt"):
    with open("auth.txt",'r') as authF:
        auth = authF.read()
else:
    auth =os.environ['AUTH_KEY']
    print(auth)

def setup(client):
    client.add_cog(Users(client,conn))
    client.add_cog(Dice(client))
    client.add_cog(Mutations(client,conn))
    client.run(auth)
    



#ACTION CARD COMMANDS --> TODO:move to seperate file
#TODO: Add commands for equipment, mutant powers, ect
@client.command(brief="List all actions")
async def list_acts(ctx):
    cur = conn.cursor()
    cur.execute("select action_name from actions;")
    await ctx.send("\n".join(["`"+x[0]+"`" for x in cur.fetchall()]))

def make_action_embed(d_response):
    e = discord.Embed(title=("**"+d_response[0]+"**"))
    yn = ["No","Yes"]
    e.add_field(name="Action Order",value=d_response[1],inline=False)
    e.add_field(name="Reaction?",value=yn[d_response[3]],inline=False)
    e.add_field(name="Effect",value=d_response[2].replace("\\n","\n"),inline=False)
    return e
        
    
@client.command(brief="Give everyone mentioned 4 action cards")
async def deal_acts(ctx, names: commands.Greedy[discord.Member]):
    if ctx.guild:
        for name in names:
            await draw_acts(name,4)
            
@client.command(brief="Draw any number of cards")
async def draw_acts(ctx,number=0):
    if number<=0:
        await ctx.send("Please specify a number")
        return
    cur = conn.cursor()
    cur.execute("select action_name,action_order,action_desc,action_reaction from actions order by random();")    
    for x in range(number):
        action_m = await ctx.send(embed=make_action_embed(cur.fetchone()))
        await action_m.add_reaction(EXIT_EMOJI)
     
#TODO: generalize the listing and info commands 
@client.command(brief="Get info about a specific action card")
async def ainfo(ctx,*,name):
    cur = conn.cursor()
    cur.execute(f"select action_name,action_order,action_desc,action_reaction from actions where action_name='{name}'")
    action = cur.fetchone()
    if action:
        action_m = await ctx.send(embed=make_action_embed(action))
        await action_m.add_reaction(EXIT_EMOJI)
    else:
        await ctx.send("`No such action`")

@client.command(brief="List all known pieces of equipment")
async def list_equips(ctx):
    cur = conn.cursor()
    cur.execute("select equip_name from equipment;")
    await ctx.send("\n".join(["`"+x[0]+"`" for x in cur.fetchall()]))

@client.command(brief="Get info about a specific piece of equipment")
async def einfo(ctx,*,name):
    cur = conn.cursor()
    cur.execute(f"select * from equipment where equip_name='{name}'")
    action = cur.fetchone()
    if action:
        action_body = action[5].replace("\\n","\n")
        astring = f"\n**{action[1]}**\nEquipment Size: {str(action[2])}\nEquipment Level: {action[3]}\nAction Order: {action[4]}\n `{action_body}`\n"
        await ctx.send(astring)
    else:
        await ctx.send(f"`ERROR:Equipment {name} not found`")
    

setup(client)

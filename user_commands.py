import discord, os, psycopg2,random, asyncio
from discord.ext import commands

class Users(commands.Cog):
    def __init__(self, bot,db_connection):
        self.bot = bot
        self.db_connection = db_connection

    @commands.command(hidden=True)
    async def refreshDB(self,ctx):
        if ctx.guild.members:
            membs = ctx.guild.members
            cur = self.db_connection.cursor()
            [cur.execute
             ("INSERT INTO users(user_dis_id,user_name) VALUES (%s,%s) ON CONFLICT DO NOTHING;",
              (usr.id,usr.name))
             for usr in membs
            ]
            self.db_connection.commit()
            self.print_usr_data(cur)
        
    @commands.command(hidden=True)
    async def mod_clone(self,ctx,name):
        await self.modify_table(ctx,name,"user_clone",1)

    @commands.command(hidden=True)
    async def mod_treason(self,ctx,name,value="1"):
        await self.modify_table(ctx,name,"user_treason",value)

    @commands.command(hidden=True)
    async def mod_xp(self,ctx,name,value):
        await self.modify_table(ctx,name,"user_xpp",value)

    @commands.command(hidden=True)
    async def mod_clearence(self,ctx,name,value):
        await self.modify_table(ctx,name,"user_clearence",value)

    @commands.command(brief="See stats about yourself")
    async def pinfo(self,ctx, name=""):
        if name=="":
            name = ctx.message.author.name
            cur = self.db_connection.cursor()
            cur.execute("select user_name,user_xpp,user_treason,user_clearence,user_clone from users where user_name='"+name+"';")
            column_names = [desc[0] for desc in cur.description]
            line1 = "`{:<15}{:<15}{:<15}{:<15}{:<15}`".format(*column_names)
            out = cur.fetchone()
        if out:
            line2 =line1+"\n"+ "`{:<15}{:<15}{:<15}{:<15}{:<15}`".format(*out)
            await ctx.send(line2)
        else:
            await ctx.send("**NO CLONE BY THAT NAME**")


    async def modify_table(self,ctx,name,column,value="1"):
        cur = self.db_connection.cursor()
        cur.execute("select user_name,"+column+" from users where user_name=\'"+name+"\';")
        user = cur.fetchone()
        try:
            value = int(value)
        except:
            value = 1
        if user:
            await ctx.send(f"**{column} of {user[0]} goes from {user[1]} to {user[1]+value}**")
            cur.execute("Update users set "+column+"=(%s) where user_name=(%s);",(user[1]+value,user[0]))
            self.db_connection.commit()
            self.print_usr_data(cur)

    def print_usr_data(self, cur):
        cur.execute("select * from users;")
        column_names = [desc[0] for desc in cur.description]
        print("{:<10}{:<25}{:<20}{:<20}{:<20}{:<20}{:<20}".format(*column_names))
        [print("{:<10}{:<25}{:<20}{:<20}{:<20}{:<20}{:<20}".format(*x)) for x in cur.fetchall()]    

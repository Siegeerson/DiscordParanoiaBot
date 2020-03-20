import discord, os, psycopg2,random, asyncio, typing
from psycopg2 import sql
from discord.ext import commands
class Mutations(commands.Cog):
    def __init__(self, bot,db_connection):
        self.bot = bot
        self.db_connection = db_connection

    def embed_mutation(self,response):
        e = discord.Embed(title="**"+response[0]+"**")
        e.add_field(name="Action Order",value=response[1],inline=False)
        e.add_field(name="Effect",value=response[2],inline=False)
        return e
        
        
    @commands.command(brief="find out information about a mutation")
    async def minfo(self,ctx,*,name):
        cur = self.db_connection.cursor()
        cur.execute("select * from mutations where mut_name=%s;",[name])
        column_names = [desc[0] for desc in cur.description]
        out = cur.fetchone()
        if out:
            await ctx.send(embed=self.embed_mutation(out))
        else:
            await ctx.send("**MUTATIONS ARE TREASONOUS**")
        

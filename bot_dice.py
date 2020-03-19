import discord, os, random
from discord.ext import commands

def adddice(out,r):
    if not out:
        out = [""]*5
    C='O '
    out[0]+="-------\t"
    out[1]+="| "+C[r<1]+" "+C[r<3]+" |\t"
    out[2]+="| "+C[r<5]+C[r&1]+C[r<5]+" |\t"
    out[3]+="| "+C[r<3]+" "+C[r<1]+" |\t"
    out[4]+="-------\t"
    return out

def rolln_dice(n=5):
    outs=""
    sum = 0
    while(n):
        print(f"{n} dice left")
        out =[]
        if n >= 3:
            for x in range(3):
                out=adddice(out,random.randint(0,5))
            outs +="\n".join(out)+"\n"
            n-=3
        else:
            for x in range(n):
                out=adddice(out,random.randint(0,5))
            outs +="\n".join(out)+"\n"
            n-=n
    return outs

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("DICE CREATED")
    @commands.command()
    async def roll(self,ctx,n :int):
        print(f"Rolling {n} dice")
        await ctx.send("**You rolled:`\n"+rolln_dice(n)+"`\nAnd the computer:`\n"+rolln_dice(1)+"`**")

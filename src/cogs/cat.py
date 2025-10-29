import discord
from discord.ext import commands
from random import randint
from api import get_cat

# no loop yet
class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def cat(self, ctx):
        random_number = randint(1, 11)
        if random_number == 11:
            await ctx.send(file=discord.File("../images/pop_cat.png"))
        else:
            cat_type = "img" if random_number >= 5 else "gif"
            data, filename = get_cat(cat_type)
            if data and filename:
                await ctx.send(file=discord.File(data, filename))
            else:
                await ctx.send("Error, cat ran away 😿")
        # elif random_number >= 5:
        #     await ctx.send(get_cat("img")[0])  
        # else :
        #     await ctx.send(get_cat("gif")[0])


async def setup(bot):
    await bot.add_cog(Cat(bot))
import discord
from discord.ext import commands
import aiohttp

async def get_pokemon(pokemon: str) -> str:
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data["sprites"]["front_default"]
            else:
                return None

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def pokemon(self, ctx, pokemon: str):
        pokemon_sprite = await get_pokemon(pokemon)

        if pokemon_sprite:
            embed = discord.Embed()
            embed.set_image(url=pokemon_sprite)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Who's that pokemon? (cause that ain't a pokemon lmao)")

async def setup(bot):
    await bot.add_cog(Pokemon(bot))
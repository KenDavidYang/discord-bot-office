import ollama
from discord.ext import commands

class Lama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = ollama.Client()
        self.model = "llama3.2"

    @commands.command()
    async def hey(self, ctx, *, prompt):
        await ctx.typing()
        response = self.client.generate(model=self.model, prompt=prompt + "keep it within 2000 characters, shorter the better, but take as much characters as you need")
        await ctx.send(response.response)


async def setup(bot):
    await bot.add_cog(Lama(bot))
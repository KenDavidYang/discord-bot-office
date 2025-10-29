from discord.ext import commands
import discord
from config import STICKERS
from database import close_db

# @bot.event

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = guild.system_channel  # Default system/welcome channel
        if channel:
            sticker = discord.Object(id=STICKERS["nervous_cat"])
            await channel.send("Thanks for inviting me! Use !register then !cookie to get a cookie...", stickers=[sticker]) # sticker limit is 3

    @commands.Cog.listener()
    async def on_shutdown(self):
        # tb fixed
        print("Bot is shutting down...")
        close_db()



async def setup(bot):
    await bot.add_cog(Events(bot))
from discord.ext import commands
from discord import app_commands
import discord
from config import GUILDS
# tb fixed
class Fabula(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="stats",
        description="Calculate your Fabula Ultima Stats",
        # guild=discord.Object(id=GUILDS["default_marketing_server"])
    )
    async def fabula_stats(self, interaction: discord.Interaction, 
                 dexterity: int,
                 insight: int,
                 might: int,
                 willpower: int,
                 level: int,
                 add_hp: int = 0,
                 add_mp: int = 0,
                 add_ip: int = 0,
                 add_def: int = 0,
                 add_mdef: int = 0
                 ):
        stats = {
            "[2;31mHP\t": (might*5) + level + add_hp,
            "[2;34mMP\t": (willpower*5) + level + add_mp,
            "[2;33mIP\t": 6 + add_ip,
            "[2;36mDEF   ": dexterity + add_def,
            "[2;35mMDEF  ": insight + add_mdef
        }

        stats_output = ''.join([f"{stats}: {value} \n" for stats, value in stats.items()])
        await interaction.response.send_message(f"Here's your stats: \n```ansi\n{stats_output}```")

async def setup(bot):
    # uncomment for specific guild or testing
    # await bot.add_cog(FabulaStats(bot), guilds=[discord.Object(id=TEST_GUILD_ID)])

    # uncomment for all guilds
    await bot.add_cog(Fabula(bot))
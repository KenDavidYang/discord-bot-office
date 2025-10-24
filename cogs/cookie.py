from discord.ext import commands
import discord
from database import cnx, is_registered
from mysql.connector import Error
from random import randint
from config import CHANNELS


async def give_cookie(bot, user):
    channel = bot.get_channel(CHANNELS["cookies"])
    try:
        if not is_registered(user):
            await channel.send(f"{user.mention}, you're not registered so no cookies for you ;(")
            await channel.send("Use !register to register (you'll get a free cookie)")
            return
        if not cnx.is_connected():
            cnx.reconnect()

        cursor = cnx.cursor()
        cursor.execute("UPDATE user_data SET cookies = cookies + 1 WHERE discord_id = %(discord_id)s", {'discord_id': user.id})

        if (randint(1, 11000) == 11):
            cursor.execute("UPDATE user_data SET milk = milk + 1 WHERE discord_id = %(discord_id)s", {'discord_id': user.id})
            await channel.send(f"{user.mention} got milk! 🥛")

        cnx.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

class Cookie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_reset()
    
    def daily_reset(self):
        cursor = cnx.cursor()
        cursor.execute("UPDATE user_data SET daily_cookie = FALSE")
        cnx.commit()
        cursor.close()

    @commands.command()
    async def cookie(self, ctx):
        cookie_channel = self.bot.get_channel(CHANNELS["cookies"])
        user = ctx.author
        cursor = cnx.cursor()
        cursor.execute("SELECT daily_cookie FROM user_data WHERE discord_id = %(user_id)s", {"user_id": user.id})
        result = cursor.fetchone()

        if is_registered(user) is None:
            await ctx.send("You are not registered yet. Please register first.")
        else:
            daily_cookie = result[0]  # True or False (stored as 1 or 0)
            if not daily_cookie:  # If daily cookie has not been claimed yet
                await cookie_channel.send(f"{user.mention} claimed a daily cookie 🍪")
                await give_cookie(self.bot, user)

                cursor.execute("UPDATE user_data SET daily_cookie = TRUE WHERE discord_id = %(user_id)s", {"user_id": user.id})
                cnx.commit()
            else:
                await ctx.send("Don't be greedy, you already claimed your daily cookie today")

        cursor.close()


async def setup(bot):
    await bot.add_cog(Cookie(bot))
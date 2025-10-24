from discord.ext import commands
from random import randint
from database import cnx
from .cookie import give_cookie
from mysql.connector import Error

class Limbo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        user = ctx.author
        username = str(user)
        discord_id = user.id

        add_user = ("INSERT INTO users (discord_id, username) VALUES (%(discord_id)s, %(username)s)")
        add_user_data = ("INSERT INTO user_data (discord_id) VALUES (%(discord_id)s)") 
        user_data = {
            "discord_id": discord_id, 
            "username": username
        }
        
        try:
            cursor = cnx.cursor()
            cursor.execute(add_user, user_data)
            cursor.execute(add_user_data, {"discord_id": discord_id} )
            cnx.commit()

            await ctx.send(f"{user.mention} has been registered! You get an appreciation cookie 🍪")
            await give_cookie(user)
        except Error as e:
            cnx.rollback()
            if e.errno == 1062:  # Duplicate entry error code
                print(f"Error: User with discord_id: {discord_id} already exists.")
                await ctx.send("User has already been registered.")
            else:
                print(f"Unexpected error: {e}")
        finally:
            if cursor:
                cursor.close()

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello! I'm your bot.")  # Sends a message in the channel

    @commands.command()
    async def d20(self, ctx):
        await ctx.send(randint(1, 20))

async def setup(bot):
    await bot.add_cog(Limbo(bot))
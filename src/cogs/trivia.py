from discord.ext import commands
import discord
from discord.ui import Button, View
from config import CHANNELS
from api import get_trivia
import html
from random import shuffle

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.trivia_channel = bot.get_channel(CHANNELS["trivia"])
        self.cookie_channel = bot.get_channel(CHANNELS["cookies"])

        self.answered_users = set()

        self._load_new_trivia()
    
    def _load_new_trivia(self):
        self.trivia = get_trivia()
        self.text = f"Trivia of The Day:\n\t{html.unescape(self.trivia['question'])}"
        self.correct_answer = html.unescape(self.trivia["correct_answer"])

        self.trivia_options = self.trivia["incorrect_answers"] + [self.trivia["correct_answer"]]
        self.trivia_options = [html.unescape(option) for option in self.trivia_options]
        shuffle(self.trivia_options)

        self.answered_users.clear()


    @commands.command()
    async def trivia(self, ctx):

        view = View(timeout=None)

        for option in self.trivia_options:
            button = Button(label=option, style=discord.ButtonStyle.primary)

            async def callback(interaction, selected_option=option):
                user = interaction.user

                if user.id in self.answered_users:
                    await interaction.response.send_message(
                        "You have already answered this question.", ephemeral=True)
                    return

                self.answered_users.add(user.id)

                if selected_option == self.correct_answer:
                    # tb fixed
                    await interaction.response.send_message(f"{selected_option} is Correct! ✅", ephemeral=True)
                    await self.cookie_channel.send(f"{user.mention} won a cookie from Trivia! 🍪")
                else:
                    await interaction.response.send_message(
                        f"{selected_option} is Incorrect! ❌\nCorrect Answer: {self.correct_answer}", ephemeral=True
                    )
            # self.button.callback = callback
            button.callback = callback
            view.add_item(button)
        
        # await self.trivia_channel.send(self.text, view=view)
        await ctx.send(self.text, view=view)
        print("trivia sent!")
    
async def setup(bot):
    await bot.add_cog(Trivia(bot))